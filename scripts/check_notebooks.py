"""Check shared notebook structure; execute only the new, explicitly offline lab.

Existing notebooks contain intentional TODOs, package magics, hosted API calls,
and saved teaching outputs. Do not execute them as unattended tests.
"""
import contextlib
import io
import sys
import warnings
from pathlib import Path
import nbformat
from IPython.core.interactiveshell import InteractiveShell

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'labs'))
transform = InteractiveShell.instance().input_transformer_manager.transform_cell
for path in sorted((root / 'labs').glob('week_*.ipynb')):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", nbformat.warnings.MissingIDFieldWarning)
        notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    namespace = {'__name__': '__main__'}
    count = 0
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != 'code':
            continue
        source = transform(cell.source)
        try:
            compile(source, f'{path.name}:cell{index}', 'exec')
        except SyntaxError as exc:
            if exc.text and '#TODO' in exc.text:
                print(f'SKIP {path.name}:cell{index}: intentional student TODO')
                continue
            raise
        if path.name == 'week_5_python_agent.ipynb':
            with contextlib.redirect_stdout(io.StringIO()):
                exec(source, namespace)
        count += 1
    print(f'PASS {path.name}: structure and syntax ({count} code cells)')
print('PASS agent extension: offline simulation; live calls disabled')
