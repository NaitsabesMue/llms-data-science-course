"""Small, inspectable teaching examples. No model calls unless explicitly requested."""

import copy
import csv
import inspect
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter


ROOT = Path(__file__).resolve().parents[1]


def load_measurements():
    with (ROOT / 'data/measurements.csv').open(newline='') as stream:
        return list(csv.DictReader(stream))


def summarize_measurements(rows):
    """Report all row counts; exclude missing measurements from means."""
    groups = sorted({row['group'] for row in rows})
    result = {}
    for group in groups:
        selected = [row for row in rows if row['group'] == group]
        values = [float(row['value']) for row in selected if row['value'] != '']
        result[group] = {
            'rows': len(selected), 'observed': len(values),
            'missing': len(selected) - len(values),
            'mean': sum(values) / len(values) if values else None,
        }
    return result


def run_agent(task, choose_action, tools, verify_final, max_steps=6):
    """Model-selected tool loop, with a caller-supplied completion verifier.

    choose_action(state) returns a dict or JSON string. Actions are
    {"tool": name, "args": {...}} or {"final": ...}. The offline labs
    use scripted policies and label them as simulations.

    max_steps bounds decisions, including invalid actions. It does not bound
    the time or cost of a blocking model/tool call; configure those in adapters.
    """
    if type(max_steps) is not int or max_steps < 1:
        raise ValueError('max_steps must be a positive integer')
    state = {'task': task, 'observations': []}
    trace = []
    start = perf_counter()
    for step in range(max_steps):
        action = None
        try:
            action = choose_action(copy.deepcopy(state))
            if isinstance(action, str):
                action = json.loads(action)
            if not isinstance(action, dict):
                raise ValueError('Action must be an object')
            if set(action) == {'final'}:
                accepted = bool(verify_final(action['final'], copy.deepcopy(state)))
                observation = {'accepted': accepted}
                trace.append({'step': step + 1, 'action': copy.deepcopy(action), 'observation': observation})
                if accepted:
                    return {'status': 'verified', 'final': action['final'], 'trace': trace,
                            'elapsed_s': perf_counter() - start}
                state['observations'].append({'tool': 'completion_check', 'result': observation})
                continue
            if set(action) != {'tool', 'args'} or not isinstance(action['tool'], str):
                raise ValueError('Expected tool/args or final')
            if action['tool'] not in tools:
                raise ValueError('Tool is not allowed')
            if not isinstance(action['args'], dict):
                raise ValueError('Tool arguments must be an object')
            function = tools[action['tool']]
            inspect.signature(function).bind(**action['args'])
            result = function(**action['args'])
            observation = {'tool': action['tool'], 'result': result}
        except Exception as exc:
            observation = {'error': f'{type(exc).__name__}: {exc}'}
        trace.append({'step': step + 1, 'action': copy.deepcopy(action), 'observation': copy.deepcopy(observation)})
        state['observations'].append(copy.deepcopy(observation))
    return {'status': 'step_limit', 'final': None, 'trace': trace,
            'elapsed_s': perf_counter() - start}


def save_run(name, payload):
    """Write exclusively to ignored local/runs; never silently overwrite a run."""
    if not re.fullmatch(r'[A-Za-z0-9_-]+', name):
        raise ValueError('Use letters, digits, underscores or hyphens in run names')
    folder = ROOT / 'local/runs'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f'{name}.json'
    record = {'recorded_at': datetime.now(timezone.utc).isoformat(), **payload}
    with target.open('x') as stream:
        json.dump(record, stream, ensure_ascii=False, indent=2, allow_nan=False)
    return target


def gemini_text(prompt):
    """Optional live call. Requires google-genai and exported environment variables.

    This is an SDK adapter, not a sandbox. Tools remain local and allowlisted.
    Configure provider timeout/cost limits before longer live experiments.
    """
    api_key, model = os.getenv('GEMINI_API_KEY'), os.getenv('GEMINI_MODEL')
    if not api_key or not model:
        raise ValueError('Set GEMINI_API_KEY and GEMINI_MODEL before a live call')
    from google import genai
    with genai.Client(api_key=api_key, http_options={'timeout': 30000}) as client:
        response = client.models.generate_content(model=model, contents=prompt,
            config={'response_mime_type': 'application/json', 'max_output_tokens': 8192})
    if not response.text:
        raise ValueError('Model returned no text')
    return response.text
