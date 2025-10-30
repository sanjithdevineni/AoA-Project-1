# Greedy EV Trip Planner

This module implements the greedy half of the Analysis of Algorithms project: plan electric vehicle charging stops along a highway to reach a destination with minimal recharging.

## Setup
- Requires Python >= 3.10.
- Dependency: matplotlib (install via `pip install -r Greedy/requirements.txt`).

## Quickstart
- Run tests: `python -m unittest`
- Generate benchmarks: `python -m Greedy.benchmark`
- Export appendix assets: `python -m Greedy.export_appendix`

Outputs are written under `Greedy/figures`, `Greedy/results`, and `Greedy/appendix`.

To include the appendix assets in LaTeX, use `\input{Greedy/appendix/code_ev_greedy.tex}` (and similarly for the other files).
