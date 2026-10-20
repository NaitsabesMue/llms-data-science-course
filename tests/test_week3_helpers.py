import importlib.util
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'labs'))
import week3_helpers as lab

ROOT = Path(__file__).resolve().parents[1]
SMALL = (ROOT / 'slides/examples/week3_churn/data.csv').read_text()
FULL = (ROOT / 'slides/examples/week3_churn/full_data.csv').read_text()


class ResultChecks(unittest.TestCase):
    def test_wrong_denominator_and_duplicate_groups_fail(self):
        rows = lab.reference_rows(SMALL)
        rows[0]['churn_rate'] = 2 / 6
        self.assertFalse(lab.check_rows(rows, SMALL)['passed'])
        rows = lab.reference_rows(SMALL)
        rows[-1] = rows[0]
        self.assertFalse(lab.check_rows(rows, SMALL)['passed'])

    def test_rounding_is_allowed_but_nonfinite_rates_and_missing_counts_fail(self):
        rows = lab.reference_rows(SMALL)
        rows[0]['churn_rate'] = 0.667
        self.assertTrue(lab.check_rows(rows, SMALL)['passed'])
        for bad in [float('nan'), float('inf'), '0.667', True]:
            rows[0]['churn_rate'] = bad
            self.assertFalse(lab.check_rows(rows, SMALL)['passed'])
        rows = lab.reference_rows(SMALL)
        del rows[0]['n_churn']
        self.assertFalse(lab.check_rows(rows, SMALL)['passed'])

    def test_small_example_hardcoded_as_full_answer_fails(self):
        self.assertFalse(lab.check_rows(lab.reference_rows(SMALL), FULL)['passed'])
        self.assertTrue(lab.check_rows(lab.reference_rows(FULL), FULL)['passed'])

    def test_json_and_unexpected_outer_structures_fail(self):
        for text in ['```json\n[]\n```', 'null', '{}', '[null]', '42']:
            self.assertFalse(lab.check_json(text, SMALL)['passed'])
        self.assertTrue(lab.check_json(json.dumps(lab.reference_rows(SMALL)), SMALL)['passed'])


class UsageChecks(unittest.TestCase):
    def response(self, **overrides):
        data = dict(prompt_token_count=100, candidates_token_count=20,
                    thoughts_token_count=5, total_token_count=125,
                    cached_content_token_count=40)
        data.update(overrides)
        return SimpleNamespace(usage_metadata=SimpleNamespace(model_dump=lambda: data),
                               model_version='test-version')

    def test_thinking_is_output_and_cache_is_not_extra_input(self):
        log = []
        lab.record_call(log, 'python', 'generation', self.response(), 'test-model')
        total = lab.usage_summary(log, 1, 2)[0]
        self.assertEqual(total['input_tokens'], 100)
        self.assertEqual(total['output_tokens_including_thinking'], 25)
        self.assertAlmostEqual(total['estimated_usd_uncached'], 0.00015)

    def test_review_and_failed_response_stay_in_total(self):
        log = []
        for stage in ['generation', 'review']:
            lab.record_call(log, 'python', stage, self.response(), 'test-model')
        total = lab.usage_summary(log, 1, 2)[0]
        self.assertEqual(total['calls'], 2)
        self.assertAlmostEqual(total['estimated_usd_uncached'], 0.0003)
        lab.record_call(log, 'python', 'network failure', None, 'test-model')
        total = lab.usage_summary(log, 1, 2)[0]
        self.assertEqual(total['calls'], 3)
        self.assertIsNone(total['input_tokens'])
        self.assertIsNone(total['estimated_usd_uncached'])

    def test_unknown_prices_and_unfamiliar_usage_are_not_zero(self):
        log = []
        lab.record_call(log, 'direct', 'request', self.response(), 'test-model')
        self.assertIsNone(lab.usage_summary(log)[0]['estimated_usd_uncached'])
        for overrides in [dict(total_token_count=999), dict(tool_use_prompt_token_count=30),
                          dict(candidates_token_count=None)]:
            log = []
            lab.record_call(log, 'direct', 'request', self.response(**overrides), 'test-model')
            self.assertIsNone(lab.usage_summary(log, 1, 2)[0]['estimated_usd_uncached'])


@unittest.skipUnless(importlib.util.find_spec('scipy'), 'Install scipy')
class IntervalChecks(unittest.TestCase):
    def interval_rows(self, csv_text):
        from scipy.stats import binomtest

        rows = lab.reference_rows(csv_text)
        for row in rows:
            bounds = binomtest(row['n_churn'], row['n_customers']).proportion_ci(method='wilson')
            row.update(ci_lower=round(float(bounds.low), 6), ci_upper=round(float(bounds.high), 6))
        return rows

    def test_formula_matches_scipy_for_full_data_and_boundary_proportions(self):
        for text in [FULL, 'contract_type,churn\nnone,0\nnone,0\nall,1\nall,1\n']:
            with self.subTest(csv=text[:40]):
                self.assertTrue(lab.check_interval_rows(self.interval_rows(text), text)['passed'])

    def test_wrong_or_missing_bounds_fail_even_with_correct_counts(self):
        for bad in [0.1, float('nan'), True, None]:
            rows = self.interval_rows(FULL)
            rows[0]['ci_lower'] = bad
            self.assertFalse(lab.check_interval_rows(rows, FULL)['passed'])
        rows = self.interval_rows(FULL)
        del rows[0]['ci_upper']
        self.assertFalse(lab.check_interval_rows(rows, FULL)['passed'])

    def test_zero_departures_does_not_produce_a_zero_width_interval(self):
        text = 'contract_type,churn\nnone,0\nnone,0\n'
        rows = self.interval_rows(text)
        rows[0]['ci_upper'] = 0.0
        self.assertFalse(lab.check_interval_rows(rows, text)['passed'])


@unittest.skipUnless(importlib.util.find_spec('pandas'), 'Install notebook dependencies')
class ExecutionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / 'local/student').mkdir(parents=True, exist_ok=True)

    def mocked_execution(self, loaded=SMALL, after=SMALL, report=None, plots=None):
        payload = dict(loaded_csv=loaded, after_csv=after,
                       report=report if report is not None else json.dumps(lab.reference_rows(SMALL)),
                       plots=plots or [])
        return dict(status='completed', exit_code=0, output=json.dumps(payload))

    def test_syntax_error_points_to_original_source_before_starting_execution(self):
        with patch.object(lab, 'DockerPythonSandbox') as docker:
            with patch.object(lab, 'LocalPythonRunner') as local:
                result = lab.run_analysis('import pandas as\ndef analyze(df): pass',
                    ROOT / 'slides/examples/week3_churn/data.csv', ROOT / 'local/student',
                    use_docker=False)
        docker.assert_not_called()
        local.assert_not_called()
        self.assertEqual(result['execution']['status'], 'syntax_error')
        self.assertIn('analysis_code', result['execution']['output'])
        self.assertIn('line 1', result['execution']['output'])
        self.assertIn('import pandas as', result['execution']['output'])

    def test_loader_row_loss_and_analysis_mutation_are_detected(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as directory:
            for execution in [self.mocked_execution(loaded=SMALL.rsplit('\n', 2)[0]+'\n'),
                              self.mocked_execution(after=SMALL.replace('two-year,0', 'two-year,1'))]:
                with patch.object(lab.DockerPythonSandbox, 'execute_python', return_value=execution):
                    result = lab.run_loader('def load_data(path): pass',
                                            ROOT / 'slides/examples/week3_churn/data.csv', directory)
                self.assertFalse(result['checks']['passed'])

    def test_timeout_is_reported_before_independent_data_checks(self):
        execution = dict(status='timeout', exit_code=None, output='', elapsed_s=60.1)
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as directory:
            with patch.object(lab.DockerPythonSandbox, 'execute_python', return_value=execution):
                with patch.object(lab, '_check_frames') as check_frames:
                    result = lab.run_loader('def load_data(path): pass',
                        ROOT / 'slides/examples/week3_churn/data.csv', directory)
            check_frames.assert_not_called()
        self.assertFalse(result['checks']['passed'])
        self.assertIn('Check docker info', result['checks']['issues'][0])
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            lab.show_run(result)
        self.assertIn('Independent checks: not run', printed.getvalue())
        self.assertIn('60.1 seconds', printed.getvalue())

    def test_valid_json_execution_can_omit_plot_when_task_requests_no_plot(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as directory:
            with patch.object(lab.DockerPythonSandbox, 'execute_python',
                              return_value=self.mocked_execution()):
                result = lab.run_analysis('def analyze(df): pass',
                    ROOT / 'slides/examples/week3_churn/data.csv', directory,
                    output_format='json', require_plot=False)
            self.assertTrue(result['checks']['passed'])

    def test_table_checked_even_when_execution_exits_successfully(self):
        bad = (ROOT / 'slides/figures/week3_churn_result.txt').read_text().replace('0.667', '0.990')
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as directory:
            with patch.object(lab.DockerPythonSandbox, 'execute_python',
                              return_value=self.mocked_execution(report=bad)):
                result = lab.run_analysis('def analyze(df): pass',
                    ROOT / 'slides/examples/week3_churn/data.csv', directory, require_plot=False)
            self.assertFalse(result['checks']['passed'])


@unittest.skipUnless(importlib.util.find_spec('pandas'), 'Install notebook dependencies')
class LocalExecutionChecks(unittest.TestCase):
    def test_interval_extension_executes_and_checks_actual_bounds(self):
        code = '''import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.stats import binomtest
def analyze(df):
    summary = df.groupby('contract_type')['churn'].agg(n_customers='size', n_churn='sum').reset_index()
    summary['churn_rate'] = summary['n_churn'] / summary['n_customers']
    bounds = [binomtest(int(k), int(n)).proportion_ci(method='wilson')
              for k, n in zip(summary.n_churn, summary.n_customers)]
    summary['ci_lower'] = [float(value.low) for value in bounds]
    summary['ci_upper'] = [float(value.high) for value in bounds]
    print(summary.to_string(index=False, float_format='{:.6f}'.format))
    fig, ax = plt.subplots()
    errors = [(summary.churn_rate - summary.ci_lower).clip(lower=0),
              (summary.ci_upper - summary.churn_rate).clip(lower=0)]
    ax.barh(summary.contract_type, summary.churn_rate, xerr=errors, capsize=4, color='teal')
    ax.set(xlim=(0, 1), xlabel='Churn rate', title='Churn by contract type: 95% Wilson intervals')
    ax.xaxis.set_major_formatter(PercentFormatter(1))
    fig.tight_layout()
'''
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as folder:
            result = lab.run_analysis(code, ROOT / 'slides/examples/week3_churn/full_data.csv', folder,
                                      use_docker=False, confidence_level=0.95)
            self.assertTrue(result['checks']['passed'], result)
            self.assertTrue(result['images'][0].read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
            # Incorrect interval output must fail even though execution and point estimates are fine.
            wrong = code.replace("summary['ci_lower'] = [float(value.low) for value in bounds]",
                                 "summary['ci_lower'] = 0.0")
            result = lab.run_analysis(wrong, ROOT / 'slides/examples/week3_churn/full_data.csv', folder,
                                      use_docker=False, confidence_level=0.95)
            self.assertFalse(result['checks']['passed'])

    def test_local_loader_and_full_analysis_produce_checked_results_and_real_plots(self):
        loader = 'import pandas as pd\ndef load_data(path):\n    return pd.read_csv(path)\n'
        initial = (ROOT / 'slides/examples/week3_churn/initial.py').read_text()
        revised = (ROOT / 'slides/examples/week3_churn/revised.py').read_text()
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as folder:
            target = Path(folder)
            with patch.object(lab, 'DockerPythonSandbox', side_effect=AssertionError('Local mode must not call Docker')):
                loading = lab.run_loader(loader, ROOT / 'slides/examples/week3_churn/data.csv', target / 'loader', use_docker=False)
                small = lab.run_analysis(initial, ROOT / 'slides/examples/week3_churn/data.csv', target / 'small', loader, use_docker=False)
                revision = lab.run_analysis(revised, ROOT / 'slides/examples/week3_churn/data.csv', target / 'revised', loader, use_docker=False)
                full = lab.run_analysis(revised, ROOT / 'slides/examples/week3_churn/full_data.csv', target / 'full', loader, use_docker=False)
            for result in [loading, small, revision, full]:
                self.assertTrue(result['checks']['passed'], result)
                self.assertEqual(result['backend'], 'local')
            self.assertEqual(loading['images'], [])
            for result in [small, revision, full]:
                self.assertTrue(result['images'][0].read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))

    def test_local_json_comparison_and_bad_results_use_independent_checks(self):
        code = '''import json
def analyze(df):
    summary = df.groupby('contract_type')['churn'].agg(n_customers='size', n_churn='sum').reset_index()
    summary['churn_rate'] = summary['n_churn'] / summary['n_customers']
    print(summary.to_json(orient='records'))
'''
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as folder:
            result = lab.run_analysis(code, ROOT / 'slides/examples/week3_churn/full_data.csv', folder,
                                      output_format='json', require_plot=False, use_docker=False)
            self.assertTrue(result['checks']['passed'], result)
            bad = lab.run_analysis(code.replace("summary['n_churn'] / summary['n_customers']", '0.99'),
                ROOT / 'slides/examples/week3_churn/full_data.csv', folder,
                output_format='json', require_plot=False, use_docker=False)
            self.assertFalse(bad['checks']['passed'])

    def test_local_input_file_changes_fail_the_original_data_check(self):
        loader = '''import pandas as pd
from pathlib import Path
def load_data(path):
    df = pd.read_csv(path)
    Path(path).write_text('contract_type,churn\\nchanged,1\\n')
    return df
'''
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as folder:
            csv_path = Path(folder) / 'input data.csv'
            csv_path.write_text(SMALL)
            result = lab.run_loader(loader, csv_path, Path(folder) / 'output', use_docker=False)
        self.assertFalse(result['checks']['passed'])
        self.assertIn('changed the input CSV', result['checks']['issues'][0])


class CSVScriptChecks(unittest.TestCase):
    script = '''import csv, json, sys
assert 'df' not in globals()
groups = {}
with open(sys.argv[1], newline='') as stream:
    for row in csv.DictReader(stream):
        counts = groups.setdefault(row['contract_type'], [0, 0])
        counts[0] += 1
        counts[1] += int(row['churn'])
print(json.dumps([{'contract_type': name, 'n_customers': n, 'n_churn': k, 'churn_rate': k / n}
                  for name, (n, k) in groups.items()]))
'''

    @classmethod
    def setUpClass(cls):
        (ROOT / 'local/student').mkdir(parents=True, exist_ok=True)

    def test_complete_script_reads_each_csv_and_reuses_on_new_data(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'local/student') as folder:
            path = Path(folder) / "customer's full data.csv"
            for text in [SMALL, FULL]:
                path.write_text(text)
                result = lab.run_csv_script(self.script, path, use_docker=False)
                self.assertTrue(result['checks']['passed'], result)
                self.assertEqual(result['backend'], 'local')
                self.assertEqual(json.loads(result['report']), lab.reference_rows(text))
                self.assertEqual(path.read_text(), text)

    def test_function_only_reply_and_incorrect_counts_fail(self):
        path = ROOT / 'slides/examples/week3_churn/full_data.csv'
        for code in ['def analyze(df):\n    print(df)',
                     'print(\'[{"contract_type":"wrong"}]\')']:
            result = lab.run_csv_script(code, path, use_docker=False)
            self.assertFalse(result['checks']['passed'])

    def test_docker_receives_the_unwrapped_script_and_mounted_path_argument(self):
        execution = dict(status='completed', exit_code=0,
                         output=json.dumps(lab.reference_rows(FULL)))
        with patch.object(lab.DockerPythonSandbox, 'execute_python', return_value=execution) as execute:
            result = lab.run_csv_script(self.script, ROOT / 'slides/examples/week3_churn/full_data.csv')
        execute.assert_called_once_with(self.script, args=['/input/data.csv'])
        self.assertTrue(result['checks']['passed'], result)


if __name__ == '__main__':
    (ROOT / 'local/student').mkdir(parents=True, exist_ok=True)
    unittest.main()
