"""Generate LaTeX appendix assets for the divide-and-conquer project."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Iterable, List

# Handle imports whether run as script or module
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))


def _read_text(path: Path) -> str:
    """Read text file content."""
    return path.read_text(encoding="utf-8")


def _listing_block(source: Path, caption: str, label: str) -> str:
    """Generate LaTeX listing block for code."""
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
    """Read first few rows of CSV file."""
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
    """Generate LaTeX table block."""
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
    """Write content to file."""
    path.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    """Generate all LaTeX appendix assets."""
    root = Path(__file__).resolve().parent
    appendix = root / "appendix"
    appendix.mkdir(parents=True, exist_ok=True)

    # Generate code listings
    listings = [
        (
            appendix / "code_max_subarray_dc.tex",
            _listing_block(
                root / "max_subarray_dc.py",
                "Divide-and-conquer maximum subarray implementation",
                "lst:dc-max-subarray",
            ),
        ),
        (
            appendix / "code_naive_baseline.tex",
            _listing_block(
                root / "naive_baseline.py",
                "Naive baseline for validation",
                "lst:dc-naive",
            ),
        ),
        (
            appendix / "code_benchmark.tex",
            _listing_block(
                root / "benchmark.py",
                "Benchmark and plotting harness",
                "lst:dc-benchmark",
            ),
        ),
    ]
    for path, content in listings:
        path.write_text(content, encoding="utf-8")

    # Generate figure references
    figs_content = "\n".join(
        [
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Divide&Conquer/figures/runtime_vs_n_dc.pdf}",
            "\\caption{Measured runtime for divide-and-conquer with reference $O(n \\log n)$ curve.}",
            "\\label{fig:dc-runtime}",
            "\\end{figure}",
            "",
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Divide&Conquer/figures/runtime_vs_n_kadane.pdf}",
            "\\caption{Measured runtime for Kadane's algorithm with reference $O(n)$ curve.}",
            "\\label{fig:kadane-runtime}",
            "\\end{figure}",
            "",
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Divide&Conquer/figures/runtime_vs_n_naive.pdf}",
            "\\caption{Measured runtime for naive algorithm with reference $O(n^2)$ curve.}",
            "\\label{fig:naive-runtime}",
            "\\end{figure}",
            "",
            "\\begin{figure}[ht]",
            "\\centering",
            "\\includegraphics[width=\\linewidth]{Divide&Conquer/figures/runtime_comparison.pdf}",
            "\\caption{Runtime comparison between divide-and-conquer and Kadane's algorithm.}",
            "\\label{fig:dc-comparison}",
            "\\end{figure}",
            "",
        ]
    )
    (appendix / "figs.tex").write_text(figs_content, encoding="utf-8")

    # Generate tables from results
    results_dir = root / "results"
    tables = []
    datasets = [
        (
            results_dir / "times_dc.csv",
            "Runtime results for divide-and-conquer algorithm",
            "tab:dc-runtime",
        ),
        (
            results_dir / "times_kadane.csv",
            "Runtime results for Kadane's algorithm",
            "tab:kadane-runtime",
        ),
        (
            results_dir / "times_naive.csv",
            "Runtime results for naive algorithm",
            "tab:naive-runtime",
        ),
        (
            results_dir / "profit_windows.csv",
            "Maximum profit windows for different data patterns",
            "tab:profit-windows",
        ),
    ]
    for path, caption, label in datasets:
        header, rows = _csv_preview(path)
        tables.append(_table_block(header, rows, caption, label))
    tables.insert(
        0, "% Run `python benchmark.py` from within Divide&Conquer folder before including these tables."
    )
    _write(appendix / "tables.tex", tables)

    print("LaTeX appendix assets generated in 'appendix/' directory.")


if __name__ == "__main__":
    main()