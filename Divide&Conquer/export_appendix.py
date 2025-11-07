"""Generate LaTeX appendix assets for the divide-and-conquer project."""

from __future__ import annotations

import sys
from pathlib import Path

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

    # Generate tables from results using pgfplotstable (reads CSV directly)
    tables_content = [
        "% Run `python benchmark.py` from within Divide&Conquer folder before including these tables.",
        "",
        "\\begin{table}[H]",
        "\\centering",
        "\\pgfplotstabletypeset[",
        "  col sep=comma,",
        "  string type,",
        "  columns={n,seconds},",
        "  every head row/.style={before row=\\toprule, after row=\\midrule},",
        "  every last row/.style={after row=\\bottomrule}",
        "]{Divide&Conquer/results/times_dc.csv}",
        "\\caption{Runtime results for divide-and-conquer algorithm}",
        "\\label{tab:dc-runtime}",
        "\\end{table}",
        "",
        "\\begin{table}[H]",
        "\\centering",
        "\\pgfplotstabletypeset[",
        "  col sep=comma,",
        "  string type,",
        "  columns={n,seconds},",
        "  every head row/.style={before row=\\toprule, after row=\\midrule},",
        "  every last row/.style={after row=\\bottomrule}",
        "]{Divide&Conquer/results/times_kadane.csv}",
        "\\caption{Runtime results for Kadane's algorithm}",
        "\\label{tab:kadane-runtime}",
        "\\end{table}",
        "",
        "\\begin{table}[H]",
        "\\centering",
        "\\pgfplotstabletypeset[",
        "  col sep=comma,",
        "  string type,",
        "  columns={n,seconds},",
        "  every head row/.style={before row=\\toprule, after row=\\midrule},",
        "  every last row/.style={after row=\\bottomrule}",
        "]{Divide&Conquer/results/times_naive.csv}",
        "\\caption{Runtime results for naive algorithm}",
        "\\label{tab:naive-runtime}",
        "\\end{table}",
        "",
        "\\begin{table}[H]",
        "\\centering",
        "\\pgfplotstabletypeset[",
        "  col sep=comma,",
        "  string type,",
        "  columns={pattern,start day,end day,window days,total profit,avg daily},",
        "  every head row/.style={before row=\\toprule, after row=\\midrule},",
        "  every last row/.style={after row=\\bottomrule}",
        "]{Divide&Conquer/results/profit_windows.csv}",
        "\\caption{Maximum profit windows for different data patterns}",
        "\\label{tab:profit-windows}",
        "\\end{table}",
        "",
    ]
    (appendix / "tables.tex").write_text("\n".join(tables_content), encoding="utf-8")

    print("LaTeX appendix assets generated in 'appendix/' directory.")


if __name__ == "__main__":
    main()