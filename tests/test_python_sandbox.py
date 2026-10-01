import json
import ast
import base64
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'labs'))
from course_tools import ROOT, run_agent, load_measurements, summarize_measurements
from python_sandbox import DockerPythonSandbox, check_analysis_execution, eda_program, save_eda_output


class SandboxTests(unittest.TestCase):
    def test_container_contract(self):
        sandbox = DockerPythonSandbox(ROOT / 'data/measurements.csv')
        command = sandbox.command('test-only')
        for option in ['--network=none', '--read-only', '--cap-drop=ALL',
                       '--security-opt=no-new-privileges', '--pull=never', '--pids-limit=32']:
            self.assertIn(option, command)
        mounts = [arg for arg in command if arg.startswith('type=bind,')]
        self.assertEqual(len(mounts), 1)
        self.assertTrue(mounts[0].endswith(',dst=/input/data.csv,readonly'))
        self.assertNotIn('--privileged', command)
        self.assertNotIn('/var/run/docker.sock', ' '.join(command))

    def test_invalid_python_is_not_executed(self):
        sandbox = DockerPythonSandbox(ROOT / 'data/measurements.csv')
        self.assertEqual(sandbox.execute_python('def :')['status'], 'syntax_error')
        with self.assertRaises(ValueError):
            sandbox.execute_python('x' * 20001)

    def test_successful_execution_still_requires_correct_results(self):
        expected = summarize_measurements(load_measurements())
        for output in ['done', json.dumps({'control': {'mean': 8.25}})]:
            check = check_analysis_execution({'status': 'completed', 'exit_code': 0, 'output': output}, expected)
            self.assertFalse(check['passed'])
        check = check_analysis_execution({'status': 'completed', 'exit_code': 0,
                                          'output': json.dumps(expected)}, expected)
        self.assertTrue(check['passed'])

    def test_eda_keeps_printed_report_and_plots(self):
        ast.parse(eda_program('def analyze(df):\n    print(df.describe())'))
        local = ROOT / 'local/student'
        local.mkdir(parents=True, exist_ok=True)
        png = b'\x89PNG\r\n\x1a\n' + b'test-payload'
        payload = {'report': 'observed means', 'plots': [base64.b64encode(png).decode()]}
        with tempfile.TemporaryDirectory(dir=local) as folder:
            report, paths = save_eda_output(json.dumps(payload), folder)
            self.assertEqual(report, 'observed means')
            self.assertEqual(paths[0].read_bytes(), png)
        with self.assertRaises(ValueError):
            save_eda_output(json.dumps(payload), ROOT / 'data')

    def test_error_feedback_drives_code_revision(self):
        # Fake sandbox observations test the loop; generated code is never executed on the host.
        expected = summarize_measurements(load_measurements())
        proposed = []
        def execute_python(code):
            proposed.append(code)
            if len(proposed) == 1:
                execution = {'status': 'completed', 'exit_code': 1, 'output': 'ValueError: empty value'}
            else:
                execution = {'status': 'completed', 'exit_code': 0, 'output': json.dumps(expected)}
            return {'execution': execution, 'checks': check_analysis_execution(execution, expected)}
        def choose(state):
            if not state['observations']:
                return {'tool': 'execute_python', 'args': {'code': 'initial code'}}
            result = state['observations'][-1]['result']
            if result['checks']['passed']:
                return {'final': result['checks']['result']}
            self.assertIn('empty value', result['execution']['output'])
            return {'tool': 'execute_python', 'args': {'code': 'revised code'}}
        def verify(final, state):
            return final == expected and any(o.get('result', {}).get('checks', {}).get('passed')
                                             for o in state['observations'])
        run = run_agent('Analyze', choose, {'execute_python': execute_python}, verify, max_steps=4)
        self.assertEqual(run['status'], 'verified')
        self.assertEqual(proposed, ['initial code', 'revised code'])


if __name__ == '__main__':
    unittest.main()
