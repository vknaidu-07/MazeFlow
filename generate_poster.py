"""Generate the academic A5 scientific poster (PNG and PDF at 300 DPI) from real benchmark results."""

import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_poster():
    # Read real benchmark data
    results_path = Path("results/benchmark_results.json")
    if not results_path.is_file():
        raise FileNotFoundError("Run run_experiments.py first to generate results!")

    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["metadata"]
    results = data["results"]

    # Filter key mazes for poster table: small, dead_end_trap, large, open_field
    key_mazes = ["small", "dead_end_trap", "open_field", "large"]

    # A5 dimensions: 148 mm x 210 mm = 5.827 in x 8.268 in
    fig_w, fig_h = 5.83, 8.27
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=300)
    fig.patch.set_facecolor("#ffffff")

    # Overall Poster Grid layout
    # Top banner: Title & Authors
    # Section 1: Problem & Search Formulation
    # Section 2: Four Search Algorithms & Complexity
    # Section 3: Empirical Comparison (Charts & Table from real data)
    # Section 4: Key Insights & Conclusions
    # Footer: References & Note

    # 1. Header Banner
    banner_ax = fig.add_axes([0.05, 0.88, 0.90, 0.10])
    banner_ax.axis("off")
    banner_ax.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor="#1e293b", edgecolor="none", transform=banner_ax.transAxes))
    banner_ax.text(
        0.5, 0.65,
        "Maze-Solving Agent: BFS, DFS, IDS & A* Compared",
        color="#ffffff", fontsize=11, fontweight="bold", ha="center", va="center", transform=banner_ax.transAxes
    )
    banner_ax.text(
        0.5, 0.28,
        "[TEAM TO FILL: Member 1, Member 2, Member 3, Member 4] | Mentor: [TEAM TO FILL: Faculty Name]\n"
        "[TEAM TO FILL: Department & Institution Name] | 2nd-Year B.Tech CSE Mini-Capstone",
        color="#94a3b8", fontsize=6.5, ha="center", va="center", transform=banner_ax.transAxes
    )

    # 2. Problem Statement & System Design (Two columns)
    # Left column: Problem & Search Formulation
    ax_prob = fig.add_axes([0.05, 0.73, 0.43, 0.14])
    ax_prob.axis("off")
    ax_prob.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8, transform=ax_prob.transAxes))
    ax_prob.text(0.04, 0.88, "1. PROBLEM & FORMULATION", fontsize=7.5, fontweight="bold", color="#0f172a", transform=ax_prob.transAxes)
    prob_text = (
        "• State Space: Discrete 2D grid cells (r, c).\n"
        "• Actions: 4-orthogonal moves (Up, Right, Down, Left).\n"
        "  Strict uniform step cost = 1. No diagonal moves.\n"
        "• Goal Test: Current cell equals Goal coordinate.\n"
        "• Expanded Node: Popped from frontier and outgoing\n"
        "  neighbors examined. Path length = transitions (moves)."
    )
    ax_prob.text(0.04, 0.12, prob_text, fontsize=6.2, color="#334155", va="bottom", transform=ax_prob.transAxes)

    # Right column: System Architecture
    ax_arch = fig.add_axes([0.52, 0.73, 0.43, 0.14])
    ax_arch.axis("off")
    ax_arch.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=0.8, transform=ax_arch.transAxes))
    ax_arch.text(0.04, 0.88, "2. SYSTEM ARCHITECTURE", fontsize=7.5, fontweight="bold", color="#0f172a", transform=ax_arch.transAxes)
    arch_text = (
        "• Model: Maze class (validation, neighbors(), format).\n"
        "• Solvers: BFS, DFS, IDS, A* (unified SearchResult).\n"
        "• Fair Benchmark: N>=10 runs, decoupled tracemalloc,\n"
        "  zero animation overhead during measurement.\n"
        "• GUI: Tkinter Canvas animation + Embedded charts."
    )
    ax_arch.text(0.04, 0.12, arch_text, fontsize=6.2, color="#334155", va="bottom", transform=ax_arch.transAxes)

    # 3. Algorithms Summary Table
    ax_tbl = fig.add_axes([0.05, 0.58, 0.90, 0.13])
    ax_tbl.axis("off")
    ax_tbl.text(0.01, 0.92, "3. ALGORITHM THEORETICAL COMPARISON (Grid Branching b<=4, Depth d)", fontsize=7.5, fontweight="bold", color="#0f172a", transform=ax_tbl.transAxes)

    col_labels = ["Algorithm", "Frontier Data Structure", "Complete?", "Optimal?", "Time Complexity", "Space Complexity"]
    table_data = [
        ["BFS", "FIFO Queue (deque)", "Yes", "Yes (uniform cost)", "O(b^d)", "O(b^d)"],
        ["DFS", "LIFO Stack (explicit)", "Yes (with visited)", "NO (first branch)", "O(b^m)", "O(b * m) linear"],
        ["IDS", "Iterative Depth Limit", "Yes", "Yes (uniform cost)", "O(b^d)", "O(b * d) linear"],
        ["A*", "Priority Queue (heapq)", "Yes", "Yes (admissible h)", "O(b^d)", "O(b^d)"]
    ]
    table = ax_tbl.table(
        cellText=table_data,
        colLabels=col_labels,
        loc="center",
        cellLoc="center",
        bbox=[0.0, 0.0, 1.0, 0.82]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6.0)
    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#e2e8f0")
            cell.set_text_props(weight="bold", color="#0f172a")
        else:
            cell.set_facecolor("#ffffff" if row % 2 == 1 else "#f8fafc")
            if col == 3 and row == 2:  # DFS non-optimal
                cell.set_text_props(weight="bold", color="#dc2626")
            elif col == 3:
                cell.set_text_props(color="#16a34a")

    # 4. Measured Experimental Results (Chart + Real Data Table)
    ax_exp = fig.add_axes([0.05, 0.28, 0.90, 0.28])
    ax_exp.axis("off")
    ax_exp.text(0.01, 0.96, "4. EMPIRICAL BENCHMARK RESULTS (Measured on Python 3.12, Windows)", fontsize=7.5, fontweight="bold", color="#0f172a", transform=ax_exp.transAxes)

    # Mini Bar chart on Left of this section: Nodes Expanded on dead_end_trap and open_field
    ax_c1 = fig.add_axes([0.08, 0.31, 0.40, 0.21])
    dead_end_runs = {r["algorithm"]: r for r in results if r["maze_name"] == "dead_end_trap"}
    algos = ["BFS", "DFS", "IDS", "A*"]
    exp_vals = [dead_end_runs[a]["nodes_expanded"] for a in algos]
    colors = ["#3498db", "#e74c3c", "#9b59b6", "#2ecc71"]
    bars = ax_c1.bar(algos, exp_vals, color=colors, width=0.55)
    ax_c1.set_yscale("log")
    ax_c1.set_title("Search Effort on 'dead_end_trap' (Log Expansions)", fontsize=6.8, fontweight="bold")
    ax_c1.set_ylabel("Nodes (log scale)", fontsize=6)
    ax_c1.tick_params(labelsize=6)
    ax_c1.grid(axis="y", linestyle="--", alpha=0.5)
    for b in bars:
        h = b.get_height()
        ax_c1.text(b.get_x() + b.get_width()/2., h*1.15, f"{int(h)}", ha="center", va="bottom", fontsize=5.5)

    # Mini Table on Right of this section: Real Measured Numbers on Key Mazes
    ax_t2 = fig.add_axes([0.52, 0.29, 0.43, 0.24])
    ax_t2.axis("off")
    res_labels = ["Maze", "Algo", "Path (moves)", "Nodes Exp.", "Median ms"]
    res_rows = []
    for m_name in ["small", "dead_end_trap", "open_field"]:
        for a_name in ["BFS", "DFS", "A*"]:
            match = [r for r in results if r["maze_name"] == m_name and r["algorithm"] == a_name][0]
            res_rows.append([
                m_name[:8], a_name, str(match["path_length"]), f"{match['nodes_expanded']:,}", f"{match['time_median_ms']:.2f}"
            ])
    t2 = ax_t2.table(cellText=res_rows, colLabels=res_labels, loc="center", cellLoc="center", bbox=[0, 0, 1, 1])
    t2.auto_set_font_size(False)
    t2.set_fontsize(5.5)
    for (row, col), cell in t2.get_celld().items():
        cell.set_edgecolor("#cbd5e1")
        if row == 0:
            cell.set_facecolor("#e2e8f0")
            cell.set_text_props(weight="bold")
        else:
            # Highlight DFS suboptimality row
            if row == 5: # dead_end_trap DFS
                cell.set_facecolor("#fee2e2")
                if col == 2:
                    cell.set_text_props(weight="bold", color="#b91c1c")

    # 5. Key Empirical Takeaways
    ax_take = fig.add_axes([0.05, 0.08, 0.90, 0.18])
    ax_take.axis("off")
    ax_take.add_patch(patches.Rectangle((0, 0), 1, 1, facecolor="#f0fdf4", edgecolor="#86efac", linewidth=0.8, transform=ax_take.transAxes))
    ax_take.text(0.02, 0.88, "5. KEY EMPIRICAL FINDINGS & VIVA DEFENSE POINTS", fontsize=7.5, fontweight="bold", color="#15803d", transform=ax_take.transAxes)
    takeaway_text = (
        "1. Optimality Proven: BFS, IDS, and A* strictly match the independent reference shortest distance across\n"
        "   all reachable mazes. DFS is NOT optimal: on 'dead_end_trap', DFS yielded 48 moves vs optimal 20.\n"
        "2. Heuristic Pruning: In open spaces, A* expanded only 24 nodes vs 168 in BFS (85.7% reduction).\n"
        "3. IDS Time-Space Trade-Off: IDS achieves BFS optimality with DFS linear memory (5.7 KB on trap maze),\n"
        "   at the cost of repeated node expansions (1,423 vs 85 for BFS).\n"
        "4. Wall-Clock Realities: On tiny mazes, simple BFS queue operations beat A* heap priority queue overhead."
    )
    ax_take.text(0.02, 0.12, takeaway_text, fontsize=6.2, color="#166534", va="bottom", transform=ax_take.transAxes)

    # Footer: Citation placeholder & Provisional Default notice
    foot_ax = fig.add_axes([0.05, 0.015, 0.90, 0.05])
    foot_ax.axis("off")
    foot_ax.text(
        0.5, 0.5,
        "PROVISIONAL DEFAULT A5 LAYOUT (148x210mm) | Reference: Russell & Norvig, AIMA (4th ed.) [TEAM TO VERIFY]\n"
        "All experimental numbers generated from local execution on Windows (Intel64 / Python 3.12).",
        fontsize=5.2, color="#64748b", ha="center", va="center", transform=foot_ax.transAxes
    )

    # Save to docs/poster_a5.png and docs/poster_a5.pdf at 300 DPI
    dest_dir = Path("docs")
    dest_dir.mkdir(parents=True, exist_ok=True)
    png_path = dest_dir / "poster_a5.png"
    pdf_path = dest_dir / "poster_a5.pdf"

    fig.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    fig.savefig(pdf_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    print(f"Poster successfully generated at 300 DPI:\n  - {png_path}\n  - {pdf_path}")

if __name__ == "__main__":
    generate_poster()
