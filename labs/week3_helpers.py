"""Supplied checks, local execution and usage accounting for the Week 3 lab.

API requests stay visible in the notebook. Execution uses Docker or a local
Python process selected by the student after inspecting the code.
"""

import ast
import csv
import io
import json
import math
from pathlib import Path
from statistics import NormalDist
import traceback

from python_sandbox import DockerPythonSandbox, LocalPythonRunner, eda_program, save_eda_output


def reference_rows(csv_text):
    """Count raw CSV rows independently of the generated pandas program."""
    groups = {}
    for row in csv.DictReader(io.StringIO(csv_text)):
        group = groups.setdefault(row['contract_type'], [0, 0])
        group[0] += 1
        group[1] += int(row['churn'])
    return [dict(contract_type=name, n_customers=count, n_churn=left,
                 churn_rate=left / count) for name, (count, left) in groups.items()]


def check_rows(rows, csv_text):
    """Check all groups, counts and rates; allow rounding to three decimals."""
    expected = {row['contract_type']: row for row in reference_rows(csv_text)}
    issues = []
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        return {'passed': False, 'issues': ['Expected a list of group objects.']}
    labels = [row.get('contract_type') for row in rows]
    if any(not isinstance(label, str) for label in labels):
        return {'passed': False, 'issues': ['Every group needs a contract_type string.']}
    if len(labels) != len(expected) or set(labels) != set(expected):
        return {'passed': False, 'issues': ['Return every contract type exactly once.']}
    for row in rows:
        name = row['contract_type']
        for field in ['n_customers', 'n_churn']:
            value = row.get(field)
            if type(value) is not int or value != expected[name][field]:
                issues.append(f"{name}: {field} should be {expected[name][field]}.")
        rate = row.get('churn_rate')
        if type(rate) not in (int, float) or not math.isclose(
                rate, expected[name]['churn_rate'], rel_tol=0, abs_tol=0.0005):
            issues.append(f"{name}: churn_rate should be {expected[name]['churn_rate']:.4f}.")
    return {'passed': not issues, 'issues': issues}


def check_json(text, csv_text):
    try:
        rows = json.loads(text)
    except (ValueError, TypeError):
        return {'passed': False, 'issues': ['The reply is not readable JSON.']}
    return check_rows(rows, csv_text)


def check_interval_rows(rows, csv_text, confidence_level=0.95):
    """Check per-group Wilson intervals independently from raw CSV counts."""
    result = check_rows(rows, csv_text)
    if not result['passed']:
        return result
    if not 0 < confidence_level < 1:
        raise ValueError('confidence_level must be between 0 and 1')
    expected = {row['contract_type']: row for row in reference_rows(csv_text)}
    z = NormalDist().inv_cdf((1 + confidence_level) / 2)
    issues = []
    for row in rows:
        name = row['contract_type']
        group = expected[name]
        n, p = group['n_customers'], group['churn_rate']
        denominator = 1 + z * z / n
        center = (p + z * z / (2 * n)) / denominator
        radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
        for field, value in [('ci_lower', max(0.0, center - radius)),
                             ('ci_upper', min(1.0, center + radius))]:
            actual = row.get(field)
            if (type(actual) not in (int, float) or not math.isfinite(actual)
                    or not 0 <= actual <= 1
                    or not math.isclose(actual, value, rel_tol=0, abs_tol=0.000001)):
                issues.append(f'{name}: {field} should be {value:.6f} (Wilson interval).')
    return {'passed': not issues, 'issues': issues}


def _check_frames(csv_path, payload, original_csv):
    import pandas as pd

    expected = pd.read_csv(io.StringIO(original_csv))
    if Path(csv_path).read_text() != original_csv:
        raise ValueError('Execution changed the input CSV file on disk.')
    for field in ['loaded_csv', 'after_csv']:
        actual = pd.read_csv(io.StringIO(payload[field]))
        pd.testing.assert_frame_equal(actual, expected, check_exact=False,
                                      rtol=1e-12, atol=1e-12)


def _execute(code, csv_path, output_dir, loader_code, include_plots=True, use_docker=True):
    backend = 'docker' if use_docker else 'local'
    result = {'checks': {'passed': False, 'issues': []}, 'report': '', 'images': [],
              'backend': backend}
    try:
        # Check each function before wrapping it, so line numbers match the student's source.
        for label, source in [('loader_code', loader_code), ('analysis_code', code)]:
            if source is not None:
                try:
                    ast.parse(source, filename=label)
                except SyntaxError as error:
                    result['execution'] = dict(
                        status='syntax_error', exit_code=None,
                        output=''.join(traceback.format_exception_only(error)),
                    )
                    result['checks']['issues'].append(
                        f'Correct {label}, inspect the repaired function, then rerun this step. '
                        'No code was executed.'
                    )
                    return result
        original_csv = Path(csv_path).read_text()
        runner = (DockerPythonSandbox(csv_path, image='llm-course-eda',
                                      timeout_s=60, output_limit=1048576)
                  if use_docker else LocalPythonRunner())
        program = eda_program(code, loader_code=loader_code, include_plots=include_plots,
                              csv_path='/input/data.csv' if use_docker else Path(csv_path).resolve())
        execution = runner.execute_python(program)
        result['execution'] = execution
        if execution['status'] != 'completed' or execution['exit_code'] != 0:
            if execution['status'] == 'timeout':
                message = 'Execution exceeded 60 seconds, including startup and Python imports. '
                if use_docker:
                    message += (
                        'Check docker info; if it also stalls, restart the Docker engine before retrying. '
                        'Alternatively, set RUN_SANDBOX = False after inspecting the code and retry. '
                    )
                message += 'The returned data has not been checked.'
            else:
                message = 'Python did not finish successfully; inspect the execution output.'
            result['checks']['issues'].append(message)
            return result
        payload = json.loads(execution['output'].strip().splitlines()[-1])
        report, images = save_eda_output(execution['output'], output_dir)
        result.update(report=report, images=images)
        _check_frames(csv_path, payload, original_csv)
        result['checks']['passed'] = True
    except Exception as error:
        result['checks']['issues'].append(f'Execution, output or unchanged-data check: {error}')
    return result


def run_loader(loader_code, csv_path, output_dir, use_docker=True):
    """Print the loaded table and check names, order, row count and values."""
    return _execute('def analyze(df):\n    print(df.to_string(index=False))\n',
                    csv_path, output_dir, loader_code, include_plots=False, use_docker=use_docker)


def run_analysis(code, csv_path, output_dir, loader_code=None,
                 output_format='table', require_plot=True, use_docker=True,
                 confidence_level=None):
    result = _execute(code, csv_path, output_dir, loader_code, use_docker=use_docker)
    if not result['checks']['passed']:
        return result
    text = Path(csv_path).read_text()
    if output_format == 'json':
        result['checks'] = check_json(result['report'], text)
    elif output_format == 'table':
        import pandas as pd
        try:
            rows = pd.read_csv(io.StringIO(result['report']), sep=r'\s+').to_dict('records')
            result['checks'] = check_rows(rows, text)
        except (ValueError, TypeError):
            result['checks'] = {'passed': False, 'issues': ['Could not read the printed group table.']}
    else:
        raise ValueError('Expected table or json output format')
    if confidence_level is not None and result['checks']['passed']:
        interval_rows = json.loads(result['report']) if output_format == 'json' else rows
        result['checks'] = check_interval_rows(interval_rows, text, confidence_level)
    if require_plot and not result['images']:
        result['checks']['passed'] = False
        result['checks']['issues'].append('The requested plot is missing.')
    return result


def run_csv_script(code, csv_path, use_docker=True):
    """Execute a complete CSV-reading script, supplying only a file-path argument."""
    result = {'backend': 'docker' if use_docker else 'local',
              'checks': {'passed': False, 'issues': []}, 'report': '', 'images': []}
    try:
        try:
            ast.parse(code, filename='comparison_script')
        except SyntaxError as error:
            result['execution'] = dict(status='syntax_error', exit_code=None,
                                      output=''.join(traceback.format_exception_only(error)))
            result['checks']['issues'].append('Correct the generated script syntax, then retry.')
            return result
        path = Path(csv_path).resolve()
        original_csv = path.read_text()
        if use_docker:
            runner = DockerPythonSandbox(path, image='llm-course-eda',
                                         timeout_s=60, output_limit=1048576)
            argument = '/input/data.csv'
        else:
            runner = LocalPythonRunner()
            argument = str(path)
        # No supplied loader, imports or DataFrame: the generated script does the work.
        execution = runner.execute_python(code, args=[argument])
        result['execution'] = execution
        if execution['status'] != 'completed' or execution['exit_code'] != 0:
            result['checks']['issues'].append('The CSV-reading script did not finish successfully.')
            return result
        result['report'] = execution['output']
        if path.read_text() != original_csv:
            result['checks']['issues'].append('The script changed the input CSV file on disk.')
            return result
        result['checks'] = check_json(result['report'], original_csv)
    except Exception as error:
        result['checks']['issues'].append(f'Script execution or result check: {error}')
    return result


def show_run(result):
    """Display actual execution evidence; never substitute an example for a run."""
    if result is None:
        print('Generated code was not executed. Use the labelled worked example below.')
        return
    from IPython.display import Image, display
    if result.get('execution'):
        print('Execution mode:', result.get('backend', 'docker'))
        execution = result['execution']
        print('Execution:', execution['status'], '; exit code:', execution['exit_code'])
        if execution.get('elapsed_s') is not None:
            print(f"Elapsed: {execution['elapsed_s']:.1f} seconds (includes process startup and imports)")
        if execution['status'] != 'completed' or execution['exit_code'] != 0:
            print(execution['output'])
            print('Independent checks: not run because execution did not finish successfully.')
            for issue in result['checks']['issues']:
                print(issue)
            return
    print(result['report'])
    for path in result['images']:
        display(Image(filename=str(path)))
    print('Independent checks:', result['checks'])


def record_call(log, route, stage, response, model):
    """Keep each response, including blocked replies or unknown usage on errors."""
    usage = getattr(response, 'usage_metadata', None)
    metadata = usage.model_dump() if usage is not None else {}
    log.append(dict(route=route, stage=stage, model=model,
                    model_version=getattr(response, 'model_version', None),
                    input_tokens=metadata.get('prompt_token_count'),
                    reply_tokens=metadata.get('candidates_token_count'),
                    thinking_tokens=metadata.get('thoughts_token_count'),
                    cached_input_tokens=metadata.get('cached_content_token_count'),
                    total_tokens=metadata.get('total_token_count'), usage_metadata=metadata))


def usage_summary(log, input_price=None, output_price=None):
    """Sum calls by route; missing usage leaves its token/cost total unknown.

    Prices are USD per million tokens, at common uncached text rates. No tools,
    cache discounts, free quota or local compute charges are priced here.
    """
    groups = {}
    for call in log:
        groups.setdefault(call['route'], []).append(call)
    result = []
    for route, calls in groups.items():
        known_input = all(c['input_tokens'] is not None for c in calls)
        known_output = all(
            c['input_tokens'] is not None and c['reply_tokens'] is not None
            and c['total_tokens'] == c['input_tokens'] + c['reply_tokens'] + (c['thinking_tokens'] or 0)
            and not c['usage_metadata'].get('tool_use_prompt_token_count') for c in calls)
        tokens_in = sum(c['input_tokens'] for c in calls) if known_input else None
        tokens_out = sum(c['reply_tokens'] + (c['thinking_tokens'] or 0)
                         for c in calls) if known_output else None
        cost = None
        if tokens_in is not None and tokens_out is not None and input_price is not None and output_price is not None:
            if not (math.isfinite(input_price) and math.isfinite(output_price)
                    and input_price >= 0 and output_price >= 0):
                raise ValueError('Prices must be finite, nonnegative USD rates.')
            cost = (tokens_in * input_price + tokens_out * output_price) / 1_000_000
        result.append(dict(route=route, calls=len(calls), input_tokens=tokens_in,
                           output_tokens_including_thinking=tokens_out,
                           estimated_usd_uncached=cost))
    return result
