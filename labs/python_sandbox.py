"""Docker execution and an explicitly selected local process for reviewed Python.

Docker uses --pull=never. LocalPythonRunner uses the current Python environment;
it provides a timeout and output limit, not container isolation.
"""

import ast
import json
import os
import selectors
import shutil
import subprocess
import sys
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

    def command(self, name, args=()):
        return [
            'docker', 'run', '--rm', '-i', '--pull=never', '--name', name,
            '--network=none', '--read-only', '--cap-drop=ALL',
            '--security-opt=no-new-privileges', '--user=65534:65534',
            '--memory=512m', '--memory-swap=512m', '--cpus=1', '--pids-limit=32',
            '--env=OPENBLAS_NUM_THREADS=1', '--env=OMP_NUM_THREADS=1',
            '--env=MKL_NUM_THREADS=1',
            '--ulimit=nofile=64:64', '--ulimit=fsize=1048576:1048576',
            '--tmpfs=/tmp:rw,noexec,nosuid,size=16m,mode=1777', '--workdir=/tmp',
            '--mount', f'type=bind,src={self.csv_path},dst=/input/data.csv,readonly',
            self.image, 'python', '-I', '-', *args,
        ]

    def execute_python(self, code, args=()):
        if not isinstance(args, (tuple, list)) or any(not isinstance(arg, str) for arg in args):
            raise TypeError('args must be a list or tuple of command-line strings')
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
                process = subprocess.Popen(self.command(name, args=args), stdin=source,
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


class LocalPythonRunner:
    """Run manually inspected code in a separate process, with normal user access."""

    def __init__(self, timeout_s=60, output_limit=1048576):
        if not 0 < timeout_s <= 60 or not 1024 <= output_limit <= 1048576:
            raise ValueError('Invalid timeout or output limit')
        self.timeout_s = timeout_s
        self.output_limit = output_limit

    def execute_python(self, code, args=()):
        if not isinstance(args, (tuple, list)) or any(not isinstance(arg, str) for arg in args):
            raise TypeError('args must be a list or tuple of command-line strings')
        if not isinstance(code, str) or not 1 <= len(code.encode()) <= 20000:
            raise ValueError('code must contain 1–20000 bytes of Python')
        try:
            ast.parse(code)
        except SyntaxError as error:
            return {'status': 'syntax_error', 'exit_code': None, 'output': str(error)}
        # Supply platform/runtime settings without forwarding notebook API keys.
        environment = {key: value for key, value in os.environ.items()
                       if key in {'PATH', 'HOME', 'USERPROFILE', 'SYSTEMROOT', 'SystemRoot',
                                  'WINDIR', 'APPDATA', 'LOCALAPPDATA', 'TMP', 'TEMP',
                                  'TMPDIR', 'LANG', 'LC_ALL', 'VIRTUAL_ENV'}}
        environment.update(OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                           MKL_NUM_THREADS='1', PYTHONIOENCODING='utf-8')
        start = time.monotonic()
        status = 'completed'
        # Keep font discovery cached across fresh Python processes.
        cache = Path(__file__).resolve().parents[1] / 'local/student/.cache/matplotlib'
        cache.mkdir(parents=True, exist_ok=True)
        environment['MPLCONFIGDIR'] = str(cache)
        with tempfile.TemporaryDirectory(prefix='week3-python-') as directory:
            with tempfile.TemporaryFile() as source, tempfile.TemporaryFile() as output:
                source.write(code.encode())
                source.seek(0)
                process = subprocess.Popen(
                    [sys.executable, '-I', '-u', '-', *args], cwd=directory, env=environment,
                    stdin=source, stdout=output, stderr=subprocess.STDOUT,
                )
                try:
                    while process.poll() is None:
                        if os.fstat(output.fileno()).st_size > self.output_limit:
                            status = 'output_limit'
                            break
                        if time.monotonic() - start >= self.timeout_s:
                            status = 'timeout'
                            break
                        time.sleep(0.05)
                    if status != 'completed':
                        process.kill()
                    process.wait(timeout=5)
                    if status == 'completed' and os.fstat(output.fileno()).st_size > self.output_limit:
                        status = 'output_limit'
                    output.seek(0)
                    captured = output.read(self.output_limit).decode(errors='replace')
                    exit_code = process.returncode if status == 'completed' else None
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.wait(timeout=5)
        return {'status': status, 'exit_code': exit_code, 'output': captured,
                'elapsed_s': time.monotonic() - start}


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


def eda_program(code, loader_code=None, include_plots=True, csv_path='/input/data.csv'):
    """Wrap the two functions for either process, retaining the same input checks."""
    if not isinstance(code, str):
        raise TypeError('Expected Python source')
    if loader_code is None:
        loader_code = "def load_data(path):\n    return pd.read_csv(path)\n"
    if not isinstance(loader_code, str):
        raise TypeError('Expected Python loader source')
    prefix = '''import os, io, json, base64, contextlib
os.environ['MPLBACKEND'] = 'Agg'
os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')
import pandas as pd
'''
    if include_plots:
        prefix += 'import matplotlib.pyplot as plt\n'
    suffix = '\ndf = load_data(' + repr(str(csv_path)) + ')\n' + '''loaded_csv = df.to_csv(index=False)
report = io.StringIO()
with contextlib.redirect_stdout(report):
    analyze(df)
plots = []
'''
    if include_plots:
        suffix += '''for number in plt.get_fignums():
    image = io.BytesIO()
    plt.figure(number).savefig(image, format='png', dpi=90, bbox_inches='tight')
    plots.append(base64.b64encode(image.getvalue()).decode('ascii'))
'''
    suffix += '''
print(json.dumps({'report': report.getvalue(), 'plots': plots,
                  'loaded_csv': loaded_csv, 'after_csv': df.to_csv(index=False)}))
'''
    return prefix + '\n' + loader_code + '\n' + code + '\n' + suffix


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
