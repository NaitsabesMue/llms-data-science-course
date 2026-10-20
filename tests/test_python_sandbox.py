import json
import ast
import base64
import tempfile
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'labs'))
from course_tools import ROOT, run_agent, load_measurements, summarize_measurements
from python_sandbox import DockerPythonSandbox, LocalPythonRunner, check_analysis_execution, eda_program, save_eda_output


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
        self.assertIn('--env=OPENBLAS_NUM_THREADS=1', command)
        self.assertEqual(sandbox.command('test-only', args=['/input/data.csv'])[-2:],
                         ['-', '/input/data.csv'])

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

    def test_loader_wrapper_does_not_import_plotting_or_statistics(self):
        source = eda_program('def analyze(df):\n    print(df.to_string(index=False))',
                             include_plots=False)
        tree = ast.parse(source)
        imports = [alias.name for node in ast.walk(tree) if isinstance(node, ast.Import)
                   for alias in node.names]
        self.assertIn('pandas', imports)
        self.assertFalse(any(name.startswith(('matplotlib', 'seaborn', 'scipy', 'numpy'))
                             for name in imports))
        self.assertFalse(any(isinstance(node, ast.Name) and node.id == 'plt'
                             for node in ast.walk(tree)))
        self.assertIn("'loaded_csv': loaded_csv", source)
        self.assertIn("'after_csv': df.to_csv(index=False)", source)

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


class LocalRunnerTests(unittest.TestCase):
    def test_script_arguments_preserve_spaces_and_quotes(self):
        argument = "customer's data file.csv"
        result = LocalPythonRunner().execute_python(
            'import sys, json\nprint(json.dumps(sys.argv[1:]))', args=[argument])
        self.assertEqual(result['exit_code'], 0)
        self.assertEqual(json.loads(result['output']), [argument])

    def test_local_process_uses_the_notebook_python_without_forwarding_api_keys(self):
        from unittest.mock import patch
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test-only'}):
            result = LocalPythonRunner().execute_python(
                "import sys, os, json\nprint(json.dumps([sys.executable, 'GEMINI_API_KEY' in os.environ]))")
        self.assertEqual(result['status'], 'completed')
        self.assertEqual(result['exit_code'], 0)
        executable, key_forwarded = json.loads(result['output'])
        self.assertEqual(executable, sys.executable)
        self.assertFalse(key_forwarded)

    def test_local_execution_retains_errors_timeout_and_output_limit(self):
        result = LocalPythonRunner().execute_python('raise ValueError("example failure")')
        self.assertNotEqual(result['exit_code'], 0)
        self.assertIn('example failure', result['output'])
        result = LocalPythonRunner(timeout_s=0.1).execute_python('import time\ntime.sleep(2)')
        self.assertEqual(result['status'], 'timeout')
        self.assertIsNone(result['exit_code'])
        result = LocalPythonRunner(output_limit=1024).execute_python('print("x" * 3000)')
        self.assertEqual(result['status'], 'output_limit')
        self.assertLessEqual(len(result['output']), 1024)


if __name__ == '__main__':
    unittest.main()
