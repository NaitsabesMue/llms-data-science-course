"""Execute generated Python in a disposable, constrained Docker container.

The host never execs generated Python. Prepare the image before class; runtime
uses --pull=never. This teaching container is not a multi-tenant sandbox service.
"""

import ast
import json
import selectors
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path


class DockerPythonSandbox:
    def __init__(self, csv_path, image='python:3.13-slim', timeout_s=20, output_limit=65536):
        self.csv_path = Path(csv_path).resolve()
        if not self.csv_path.is_file() or ',' in str(self.csv_path):
            raise ValueError('Expected a CSV file path without commas')
        if not 1 <= timeout_s <= 60 or not 1024 <= output_limit <= 1048576:
            raise ValueError('Invalid timeout or output limit')
        self.image = image
        self.timeout_s = timeout_s
        self.output_limit = output_limit

    def command(self, name):
        return [
            'docker', 'run', '--rm', '-i', '--pull=never', '--name', name,
            '--network=none', '--read-only', '--cap-drop=ALL',
            '--security-opt=no-new-privileges', '--user=65534:65534',
            '--memory=512m', '--memory-swap=512m', '--cpus=1', '--pids-limit=32',
            '--ulimit=nofile=64:64', '--ulimit=fsize=1048576:1048576',
            '--tmpfs=/tmp:rw,noexec,nosuid,size=16m,mode=1777', '--workdir=/tmp',
            '--mount', f'type=bind,src={self.csv_path},dst=/input/data.csv,readonly',
            self.image, 'python', '-I', '-',
        ]

    def execute_python(self, code):
        if not isinstance(code, str) or not 1 <= len(code.encode()) <= 20000:
            raise ValueError('code must contain 1–20000 bytes of Python')
        # This is a syntax check only. Container isolation enforces execution limits.
        try:
            ast.parse(code)
        except SyntaxError as exc:
            return {'status': 'syntax_error', 'exit_code': None, 'output': str(exc)}
        if not shutil.which('docker'):
            raise RuntimeError('Install and start Docker, then prepare the image before class')
        name = 'course-python-' + uuid.uuid4().hex
        output = bytearray()
        status = 'completed'
        start = time.monotonic()
        process = None
        try:
            with tempfile.TemporaryFile() as source:
                source.write(code.encode()); source.seek(0)
                process = subprocess.Popen(self.command(name), stdin=source,
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ)
                    while selector.get_map():
                        remaining = self.timeout_s - (time.monotonic() - start)
                        if remaining <= 0:
                            status = 'timeout'
                            break
                        for key, _ in selector.select(min(remaining, 0.2)):
                            chunk = key.fileobj.read1(8192)
                            if not chunk:
                                selector.unregister(key.fileobj)
                                continue
                            capacity = self.output_limit - len(output)
                            output.extend(chunk[:capacity])
                            if len(chunk) > capacity:
                                status = 'output_limit'
                                break
                        if status != 'completed':
                            break
                if status == 'completed':
                    try:
                        remaining = max(0.01, self.timeout_s - (time.monotonic() - start))
                        exit_code = process.wait(timeout=remaining)
                    except subprocess.TimeoutExpired:
                        status = 'timeout'
                if status != 'completed':
                    process.kill()
                    process.wait(timeout=5)
                    exit_code = None
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.wait(timeout=5)
            if process is not None:
                process.stdout.close()
            # A timed-out client may leave its container running: remove it by its unique name.
            try:
                subprocess.run(['docker', 'rm', '-f', name], capture_output=True, timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                pass
        return {'status': status, 'exit_code': exit_code,
                'output': output.decode(errors='replace'), 'elapsed_s': time.monotonic() - start}


def check_analysis_execution(execution, expected):
    """Check the computation outside the sandbox; no model-generated tests run here."""
    if execution.get('status') != 'completed' or execution.get('exit_code') != 0:
        return {'passed': False, 'issues': ['Python execution did not complete successfully']}
    try:
        result = json.loads(execution['output'])
    except (ValueError, KeyError):
        return {'passed': False, 'issues': ['Print exactly one JSON object as the program output']}
    if result != expected:
        return {'passed': False, 'issues': ['Group counts, missing counts, or observed means do not match the data']}
    return {'passed': True, 'issues': [], 'result': result}


def eda_program(code):
    """Wrap the original analyze(df) exercise for execution inside the container."""
    if not isinstance(code, str):
        raise TypeError('Expected Python source')
    prefix = '''import os, io, json, base64, contextlib
os.environ['MPLBACKEND'] = 'Agg'
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib'
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
'''
    suffix = '''
report = io.StringIO()
with contextlib.redirect_stdout(report):
    analyze(pd.read_csv('/input/data.csv'))
plots = []
for number in plt.get_fignums():
    image = io.BytesIO()
    plt.figure(number).savefig(image, format='png', dpi=90, bbox_inches='tight')
    plots.append(base64.b64encode(image.getvalue()).decode('ascii'))
print(json.dumps({'report': report.getvalue(), 'plots': plots}))
'''
    return prefix + '\n' + code + '\n' + suffix


def save_eda_output(output, folder):
    """Save returned plot bytes locally; never use a model-supplied filename."""
    import base64
    # Top-level generated prints may precede the wrapper's final JSON line.
    payload = json.loads(output.strip().splitlines()[-1])
    if not isinstance(payload.get('report'), str) or not isinstance(payload.get('plots'), list):
        raise ValueError('Expected a report and a list of PNG plots')
    if len(payload['plots']) > 10:
        raise ValueError('Too many plots')
    target = Path(folder).resolve()
    local_student = Path(__file__).resolve().parents[1] / 'local/student'
    if not target.is_relative_to(local_student.resolve()):
        raise ValueError('Save private EDA output under local/student')
    target.mkdir(parents=True, exist_ok=True)
    paths = []
    for index, encoded in enumerate(payload['plots'], start=1):
        data = base64.b64decode(encoded, validate=True)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Expected PNG data')
        path = target / f'plot_{index}.png'
        path.write_bytes(data)
        paths.append(path)
    return payload['report'], paths
