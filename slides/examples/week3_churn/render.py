"""Run the reviewed lecture examples and regenerate their actual outputs.

From the repository root, with pandas and matplotlib installed:
    MPLBACKEND=Agg python slides/examples/week3_churn/render.py

These are fixed teaching examples, not captured Gemini responses. This script
runs the reviewed source locally to prepare reusable course figures. Live,
unreviewed model code continues to use the notebook's Docker execution helper.
full_data.csv freezes the notebook's 600-row synthetic-data generator, using
seed 42 and NumPy 2.5.4, so the lecture's inputs are available for inspection.
"""

import contextlib
import csv
import io
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import initial
import revised


def render_and_check(name, module, data_path, figures):
    # Count from the raw CSV independently of the pandas calculation.
    expected = {}
    with data_path.open(newline="") as stream:
        for row in csv.DictReader(stream):
            group = expected.setdefault(row["contract_type"], [0, 0])
            group[0] += 1
            group[1] += int(row["churn"])
    labels = list(expected)
    rates = [left / count for count, left in expected.values()]

    df = pd.read_csv(data_path)
    original = df.copy(deep=True)
    plt.close("all")
    with contextlib.redirect_stdout(io.StringIO()) as output:
        module.analyze(df)
    report = output.getvalue()
    result = pd.read_csv(io.StringIO(report), sep=r"\s+")
    assert list(result["contract_type"]) == labels
    for row, label, rate in zip(result.itertuples(), labels, rates):
        assert (row.n_customers, row.n_churn) == tuple(expected[label])
        assert math.isclose(row.churn_rate, rate, abs_tol=0.0005)
    pd.testing.assert_frame_equal(df, original)

    figure = plt.gcf()
    axes = figure.axes[0]
    assert len(axes.patches) == len(rates)
    if name == "initial":
        plotted = [bar.get_height() for bar in axes.patches]
        assert [tick.get_text() for tick in axes.get_xticklabels()] == labels
        assert axes.get_ylim() == (0, 1)
    else:
        plotted = [bar.get_width() for bar in axes.patches]
        assert [tick.get_text() for tick in axes.get_yticklabels()] == labels
        assert axes.get_xlim() == (0, 1)
        assert [text.get_text() for text in axes.texts] == [
            f"{rate:.1%}" for rate in rates
        ]
    assert all(math.isclose(a, b) for a, b in zip(plotted, rates))
    figure.savefig(figures / f"week3_churn_{name}.png", dpi=200)
    plt.close("all")
    return report, sum(count for count, _ in expected.values())


def main():
    folder = Path(__file__).resolve().parent
    figures = folder.parents[1] / "figures"
    figures.mkdir(exist_ok=True)
    initial_report, _ = render_and_check("initial", initial, folder / "data.csv", figures)
    revised_report, _ = render_and_check("revised", revised, folder / "data.csv", figures)
    assert initial_report == revised_report, "A plot revision must preserve these numbers."
    (figures / "week3_churn_result.txt").write_text(initial_report)

    full_report, row_count = render_and_check("full", revised, folder / "full_data.csv", figures)
    assert row_count == 600
    (figures / "week3_churn_full_result.txt").write_text(full_report)
    print("Six-row example:")
    print(initial_report, end="")
    print("Full dataset:")
    print(full_report, end="")
    print("PASS: every table and plot matches independent CSV counts.")
    print("PASS: the plot revision preserves the small-example results and input rows.")
    print("PASS: the same revised function analyses all 600 full-data rows.")
    print(f"Rendered with pandas {pd.__version__}, matplotlib {matplotlib.__version__}.")


if __name__ == "__main__":
    main()
