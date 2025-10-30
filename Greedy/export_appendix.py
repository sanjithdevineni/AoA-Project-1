"""Generate LaTeX appendix assets for the greedy EV project."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _listing_block(source: Path, caption: str, label: str) -> str:
    code = _read_text(source).rstrip()
    return (
        "\\begin{lstlisting}[caption={"
        + caption
        + "},label={"
        + label
        + "}]\n"
        + code
        + "\n\\end{lstlisting}\n"
    )


def _csv_preview(path: Path, limit: int = 5) -> tuple[List[str], List[List[str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader, [])
        rows = []
        for row in reader:
            rows.append(row)
            if len(rows) >= limit:
                break
    return header, rows


def _table_block(
    header: List[str],
    rows: List[List[str]],
    caption: str,
    label: str,
) -> str:
    if not header:
        return f"% data missing for {label}\n"
    alignment = " ".join("r" for _ in header)
    lines = [
        "\\begin{table}[ht]",
        "\\centering",
        f"\\begin{{tabular}}{{{alignment}}}",
        " " + " & ".join(header) + " \\\\",
        " \\hline",
    ]
    for row in rows:
        lines.append(" " + " & ".join(row) + " \\\\")
    lines.extend(
        [
            "\\end{tabular}",
            f"\\caption{{{caption}}}",
            f"\\label{{{label}}}",
            "\\end{table}",
            "",
        ]
    )
    return "\n".join(lines)


def _write(path: Path, content: Iterable[str]) -> None:
    path.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    appendix = root / "appendix"
    appendix.mkdir(parents=True, exist_ok=True)

    listings = [
        (
            appendix / "code_ev_greedy.tex",
            _listing_block(root / "ev_greedy.py", "Greedy EV planner implementation", "lst:ev-greedy"),
        ),
        (
            appendix / "code_naive_baseline.tex",
            _listing_block(
                root / "naive_baseline.py",
                "Dynamic programming baseline for validation",
                "lst:ev-naive",
            ),
        ),
        (
            appendix / "code_benchmark.tex",
            _listing_block(
                root / "benchmark.py",
                "Benchmark and plotting harness",
                "lst:ev-benchmark",
            ),
        ),
    ]
    for path, content in listings:
        path.write_text(content, encoding="utf-8")

    figs_content = "\n".join(
        [
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Greedy/figures/runtime_vs_n_sorted.pdf}",
            "\\caption{Measured runtime for presorted inputs with a reference $O(n)$ curve.}",
            "\\label{fig:runtime-sorted}",
            "\\end{figure}",
            "",
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Greedy/figures/runtime_vs_n_unsorted.pdf}",
            "\\caption{Measured runtime including sorting with a reference $O(n \\log n)$ curve.}",
            "\\label{fig:runtime-unsorted}",
            "\\end{figure}",
            "",
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Greedy/figures/stops_vs_R.pdf}",
            "\\caption{Charging stops required as the vehicle range varies.}",
            "\\label{fig:stops-vs-r}",
            "\\end{figure}",
            "",
        ]
    )
    (appendix / "figs.tex").write_text(figs_content, encoding="utf-8")

    results_dir = root / "results"
    tables = []
    datasets = [
        (
            results_dir / "times_sorted.csv",
            "Runtime results for presorted inputs",
            "tab:runtime-sorted",
        ),
        (
            results_dir / "times_unsorted.csv",
            "Runtime results for unsorted inputs",
            "tab:runtime-unsorted",
        ),
        (
            results_dir / "stops_vs_R.csv",
            "Stops as a function of vehicle range",
            "tab:stops-vs-r",
        ),
    ]
    for path, caption, label in datasets:
        header, rows = _csv_preview(path)
        tables.append(_table_block(header, rows, caption, label))
    tables.insert(0, "% Run `python -m Greedy.benchmark` before including these tables.")
    _write(appendix / "tables.tex", tables)


if __name__ == "__main__":
    main()
