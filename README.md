# Maze-Solving Agent: BFS, DFS, Iterative Deepening and A* Compared

A comprehensive 2nd-year B.Tech CSE AI Mini-Capstone Project comparing classical state-space search algorithms on 2D grid mazes using real empirical benchmarks, automated tests, and an interactive desktop visualization.

[![Python Version](https://img.shields.io/badge/Python-3.10%2B%20%7C%203.12.10-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![Charts](https://img.shields.io/badge/Charts-Matplotlib-orange.svg)](https://matplotlib.org/)
[![Tests](https://img.shields.io/badge/Tests-35%20Passing%20(pytest)-brightgreen.svg)](https://docs.pytest.org/)
[![Academic Deliverables](https://img.shields.io/badge/Deliverables-Report%20%7C%20A5%20Poster%20%7C%20Viva%20Q%26A-purple.svg)](docs/)

---

## 1. Project Overview

Finding a shortest or feasible path from a start state to a goal state while avoiding obstacles is a fundamental problem in Artificial Intelligence. This project implements, visualizes, and rigorously evaluates four foundational search strategies:
1. **Breadth-First Search (BFS)**: Uninformed, FIFO queue, guaranteed optimal path under uniform costs.
2. **Depth-First Search (DFS)**: Uninformed, explicit LIFO stack, non-optimal exploration that reveals the danger of premature branch commitment.
3. **Iterative Deepening Search (IDS)**: Uninformed, repeated depth-limited DFS, combines BFS optimality with DFS linear memory footprint.
4. **A\* Search (A-Star)**: Informed heuristic search using the Manhattan distance, delivering optimal paths with heuristic pruning.

All four algorithms operate on an **identical 2D grid state representation** with **strictly standardized orthogonal movement rules** (Up, Right, Down, Left).

---

## 2. Key Features

- **Interactive Web Application (`web/`)**:
  - Modern Cyber-Academic Dark Glassmorphism interface accessible from any browser.
  - Dual modes: **Interactive Single Solver** with timeline scrubbing and **4-Way Multi-Algorithm Live Race** running BFS, DFS, IDS, and A* simultaneously.
  - High-performance HTML5 Canvas renderer with glowing laser path, frontier halos, and cell inspection HUD.
  - Built-in **Benchmark Studio** and **Theoretical Complexity Guide** with live SVG charts and CSV/JSON export.
  - Launch easily via `run_web.bat` or `python -m http.server 8080 --directory web`.
- **Interactive Desktop GUI (Tkinter)**:
  - Dynamic grid rendering with color-coded exploration (Start, Goal, Walls, Explored cells, Frontier, Solution path).
  - Non-blocking animation playback using `root.after()` with pause, resume, single-step, reset, and animation speed slider.
  - Interactive maze editor: draw walls, erase walls, relocate Start, relocate Goal.
  - Preset loader with 11 benchmark mazes + Seeded Deterministic Generators (Randomized DFS Perfect Maze & Obstacle Grid).
  - Embedded **Comparison Dashboard** featuring live data tables and embedded Matplotlib bar charts.
- **Fair Empirical Benchmark Engine (`run_experiments.py`)**:
  - Decoupled execution: Zero GUI or print overhead during timing runs.
  - Statistical rigor: 1 untimed warm-up run + $N \ge 10$ timed runs reporting median, mean, min, max, and standard deviation.
  - Isolated peak memory profiling via Python's `tracemalloc`.
  - Automatic export of results to `results/benchmark_results.csv`, `results/benchmark_results.json`, and `results/comparison_charts.png`.
- **Comprehensive Automated Test Suite (`tests/`)**:
  - 35 unit and regression tests executed via `python -m pytest -q`.
  - Independent reference BFS solver verifies mathematical optimality.
  - Large-maze recursion safety testing on $41 \times 41$ grids.
  - Headless GUI smoke testing.
- **Academic Deliverables Generated from Real Data**:
  - [`docs/REPORT_TEMPLATE.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/REPORT_TEMPLATE.md): Complete capstone report with real numbers and theoretical proofs.
  - [`docs/POSTER_A5.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/POSTER_A5.md): Printable A5 poster layout, plus generated [`docs/poster_a5.png`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/poster_a5.png) and [`docs/poster_a5.pdf`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/poster_a5.pdf) at 300 DPI.
  - [`docs/PRESENTATION_OUTLINE.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/PRESENTATION_OUTLINE.md): 12-slide review presentation with detailed speaking notes.
  - [`docs/VIVA_QA.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/VIVA_QA.md): 25+ comprehensive viva questions with rigorous academic answers.
  - [`docs/TEAM_PLAN.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/TEAM_PLAN.md): 4-member work division, owned files, and rehearsal checklists.

---

## 3. Technology Stack & Design Justification

- **Language**: Python 3.12 (Python 3.10+ supported).
- **GUI**: Standard Python `tkinter` & `ttk`.
  - *Why Tkinter*: Ships natively with standard Windows Python installations. Zero external C-library compilation issues, lightweight, instantly accessible to 2nd-year students, and reliable on low-spec lab laptops.
- **Data Visualization**: `matplotlib` (embedded in Tkinter via `FigureCanvasTkAgg` and exported to 300 DPI publication charts).
- **Test Framework**: `pytest`.
- **Standard Library Components**:
  - `collections.deque`: $O(1)$ push/pop for BFS queue.
  - `heapq`: Min-heap priority queue for A* with 4-tuple deterministic tie-breaking.
  - `tracemalloc`: Isolated heap memory tracking.
  - `dataclasses`: Standardized `SearchResult` interface.
  - `time.perf_counter`: High-resolution monotonic timing.

---

## 4. Directory Structure

```text
c:\Users\kushw\OneDrive\Desktop\AI\
├── main.py                     # Desktop GUI application entry point
├── run_experiments.py          # CLI benchmark runner with argparse
├── generate_poster.py          # Script to generate A5 poster PNG/PDF at 300 DPI
├── requirements.txt            # Runtime dependencies (matplotlib)
├── requirements-dev.txt        # Development dependencies (pytest)
├── README.md                   # This project guide
├── src/
│   └── maze_agent/
│       ├── __init__.py
│       ├── maze.py             # 2D Grid model, validation, parsing, neighbors()
│       ├── maze_library.py     # 11 preset mazes + seeded deterministic generators
│       ├── algorithms/
│       │   ├── __init__.py
│       │   ├── common.py       # SearchResult dataclass & Manhattan distance
│       │   ├── bfs.py          # Breadth-First Search
│       │   ├── dfs.py          # Depth-First Search (Iterative stack)
│       │   ├── ids.py          # Iterative Deepening Search (min_depth cycle suppression)
│       │   └── astar.py        # A* Search (heapq + deterministic tie-breaking)
│       ├── evaluation/
│       │   ├── __init__.py
│       │   ├── benchmark.py    # Fair timing and tracemalloc memory engine
│       │   └── export.py       # CSV, JSON, and Matplotlib chart generator
│       └── gui/
│           ├── __init__.py
│           ├── app.py          # Main Tkinter window & animation scheduler
│           ├── grid_view.py    # Tkinter Canvas rendering & interactive mouse editor
│           └── dashboard.py    # Embedded benchmark comparison table & charts
├── mazes/                      # Predefined maze text files (.txt)
├── tests/
│   ├── test_maze.py            # Unit tests for maze parsing, validation, neighbors
│   ├── test_algorithms.py      # Correctness & optimality tests with reference BFS
│   ├── test_benchmark.py       # Benchmark and export tests
│   └── test_gui_smoke.py       # Headless GUI lifecycle smoke test
├── results/                    # Generated experimental data (never hand-edited)
│   ├── benchmark_results.csv   # Raw benchmark metrics
│   ├── benchmark_results.json  # Full JSON metrics with environment metadata
│   └── comparison_charts.png   # 4-panel Matplotlib comparison figure
└── docs/
    ├── ASSUMPTIONS.md          # Engineering and academic design decisions
    ├── OFFICIAL_GUIDELINES.md  # Placeholder for official syllabus guidelines
    ├── IMPLEMENTATION_PLAN.md  # Milestone roadmap and architecture
    ├── REPORT_TEMPLATE.md      # Mini-capstone project report with real metrics
    ├── POSTER_A5.md            # A5 poster specifications
    ├── poster_a5.png           # 300 DPI high-resolution poster image
    ├── poster_a5.pdf           # 300 DPI vector printable poster PDF
    ├── PRESENTATION_OUTLINE.md # 12-slide review presentation with speaking notes
    ├── VIVA_QA.md              # 25+ comprehensive viva questions and answers
    └── TEAM_PLAN.md            # 4-member ownership plan and rehearsal guide
```

---

## 5. Prerequisites & Windows Setup Instructions

### Prerequisites
- Windows 10 or 11 (64-bit)
- Python 3.10 or higher (Python 3.12.10 recommended)

### Setup in PowerShell (Recommended)
Open PowerShell inside this directory (`c:\Users\kushw\OneDrive\Desktop\AI`):

```powershell
# 1. Create a virtual environment
py -m venv .venv

# 2. Activate the virtual environment
# Note: If PowerShell blocks script execution, run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install runtime dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Install testing and development dependencies
pip install -r requirements-dev.txt
```

### Setup in Windows Command Prompt (`cmd.exe`)
```cmd
:: 1. Create a virtual environment
py -m venv .venv

:: 2. Activate the virtual environment
.venv\Scripts\activate.bat

:: 3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

---

## 6. How to Run

### 6.1 Launch the Web Application (Browser)
```powershell
# Option A: One-click batch or PowerShell runner
.\run_web.bat
# or
.\run_web.ps1

# Option B: Standard Python local web server
python -m http.server 8080 --directory web
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser to experience:
- Modern glassmorphism UI with interactive wall painting and timeline scrubbing.
- **4-Way Algorithm Live Race Mode** with synchronized real-time competition.
- Built-in **Benchmark Studio** with live dynamic SVG charts and CSV/JSON export.

### 6.2 Launch the Desktop GUI (Tkinter)
```bash
python main.py
```
- Select an algorithm (BFS, DFS, IDS, A*) from the dropdown.
- Click **▶ Run** to animate the search process.
- Click **📊 Compare All (Benchmark Dashboard)** to run all four algorithms on the current maze and view the side-by-side comparison table and Matplotlib charts.
- Use the **Grid Editor** radio buttons to draw/erase walls or move the Start and Goal locations.

### 6.2 Run Automated Tests
```bash
python -m pytest -q
```
*Expected Output*: `35 passed in ~3.0s (100% green)`.

### 6.3 Run Benchmark Experiments from the CLI
```bash
# Run full benchmark suite (10 repetitions per algorithm across all 11 mazes)
python run_experiments.py --repetitions 10

# Quick run (3 repetitions on small and trap mazes)
python run_experiments.py -n 3 --mazes small,dead_end_trap

# Skip memory measurement to run faster
python run_experiments.py --no-memory
```
All outputs are automatically saved to `results/`.

### 6.4 Re-generate the A5 Scientific Poster
```bash
python generate_poster.py
```
Outputs high-resolution 300 DPI files to `docs/poster_a5.png` and `docs/poster_a5.pdf`.

---

## 7. Academic Definitions & Optimality Notes

### Definition of "Expanded Node"
A node is counted as **expanded** strictly when it is removed from the frontier (queue/stack/priority queue) and its outgoing orthogonal neighbors are generated and examined.
- Start node counts as 1 expansion if Start $\ne$ Goal.
- If Start == Goal: `nodes_expanded = 0`, `path_length = 0`.
- Stale nodes popped from priority queue and skipped are **not** counted as expansions.

### Definition of "Path Length"
Defined strictly as the number of **moves** (edge transitions), which equals $\text{len}(path) - 1$. If no path exists, `path_length = None`.

### Algorithm Summary Table

| Algorithm | Complete? | Optimal? (Uniform Cost) | Time Complexity | Space Complexity | Best Used For |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **BFS** | Yes | **Yes** | $O(b^d)$ | $O(b^d)$ | Small-to-medium graphs where shortest path is required. |
| **DFS** | Yes (with visited set) | **NO** | $O(b^m)$ | $O(bm)$ | Memory-constrained exploration when any path suffices. |
| **IDS** | Yes | **Yes** | $O(b^d)$ | $O(bd)$ | Large search spaces where optimality is needed with linear memory. |
| **A\*** | Yes | **Yes** (with admissible $h$) | $O(b^d)$ | $O(b^d)$ | Targeted pathfinding when a quality heuristic is available. |

---

## 8. Real Experimental Findings & Data Interpretation

*The following conclusions are drawn directly from our measured data in `results/benchmark_results.json` on Windows 11 (Intel64, Python 3.12.10):*

1. **DFS Non-Optimality Proven**: On `dead_end_trap` ($13 \times 13$), BFS, IDS, and A* all identified the true shortest path of **20 moves**. DFS plunged down its initial branch and returned a circuitous detour of **48 moves** (140% longer!).
2. **Heuristic Pruning Efficiency**: In `open_field` ($15 \times 15$), BFS expanded **168 nodes** in a wide diamond pattern. Guided by Manhattan distance, A* expanded only **24 nodes**—a direct beam straight to the goal—achieving an **85.7% reduction** in search effort.
3. **IDS Time-Memory Trade-Off**: IDS achieved BFS optimality while using only **5.7 KB** peak memory on `dead_end_trap` (vs **16.2 KB** for BFS). However, it required **1,423 cumulative expansions** across 21 depth iterations, consuming **2.249 ms** versus BFS's **0.100 ms**. On `large` ($41 \times 41$), this re-expansion reached **46,989 nodes** and **77.430 ms**.
4. **The Heap Constant-Factor Effect**: On `medium` ($21 \times 21$), both BFS and A* expanded 174 nodes, but BFS completed in **0.197 ms** compared to **0.278 ms** for A*. Python's `heapq` priority queue involves $O(\log N)$ tuple comparisons, whereas BFS operates via highly optimized $O(1)$ C-level double-ended queue operations in `collections.deque`. Theoretical expansion counts do not always translate to faster wall-clock time on small graphs.

> **Hardware Context**: Exact execution timings depend on processor speed and operating system background tasks. The relative rankings and expansion counts remain strictly reproducible.

---

## 9. Troubleshooting Guide for Windows

- **Problem**: `Activate.ps1 cannot be loaded because running scripts is disabled on this system.`  
  **Solution**: Open PowerShell and run:  
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`  
  Then re-run `.venv\Scripts\Activate.ps1`.
- **Problem**: `'python' is not recognized as an internal or external command.`  
  **Solution**: Run using the Python launcher `py main.py` or specify the full path to `python.exe` in your virtual environment.
- **Problem**: `ModuleNotFoundError: No module named 'tkinter'.`  
  **Solution**: In standard Python on Windows, Tkinter is included by default. If using a customized minimal Python distribution, re-run the Python Windows installer, select "Modify", and check "tcl/tk and IDLE".
- **Problem**: `High-DPI display causes blurry or oversized canvas.`  
  **Solution**: Windows display scaling is supported automatically. You can also resize the window, and the Canvas cell size will dynamically auto-scale to fit the screen.

---

## 10. Official Guidelines & Faculty Review Notice

All templates, poster layouts, and team divisions currently follow **PROVISIONAL DEFAULT** settings.  
When official project guidelines, formatting rubrics, or review schedules are announced by your lecturer, paste them into:  
👉 [`docs/OFFICIAL_GUIDELINES.md`](file:///c:/Users/kushw/OneDrive/Desktop/AI/docs/OFFICIAL_GUIDELINES.md)
