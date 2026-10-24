"""Entry point for Maze-Solving Agent Application.

Dual-Mode Entrypoint:
1. Desktop GUI: Launch interactive Tkinter window when run directly (`python main.py`).
2. Cloud / Vercel Serverless: Exports WSGI `app`, `application`, and `handler` for
   hosting the interactive web application and REST API endpoints.
"""

from __future__ import annotations

import json
import mimetypes
import os
from pathlib import Path
import sys
from typing import Callable, Iterable, List, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WEB_DIR = PROJECT_ROOT / "web"


def _build_response(
    start_response: Callable,
    status: str,
    headers: List[Tuple[str, str]],
    body: bytes,
) -> Iterable[bytes]:
    """Helper to finalize HTTP response with Content-Length."""
    # Ensure Content-Length is set if not already present
    header_names = {h[0].lower() for h in headers}
    if "content-length" not in header_names:
        headers.append(("Content-Length", str(len(body))))
    if "access-control-allow-origin" not in header_names:
        headers.append(("Access-Control-Allow-Origin", "*"))

    start_response(status, headers)
    return [body]


def app(environ: dict, start_response: Callable) -> Iterable[bytes]:
    """WSGI application callable for Vercel Serverless Python runtime.

    Handles:
    - Web static asset serving (`/`, `/style.css`, `/js/...`)
    - REST API endpoints:
        GET  /api/health   - System health check
        GET  /api/mazes    - List of predefined benchmark mazes
        POST /api/solve    - Run BFS, DFS, IDS, or A* on a maze
    """
    method = environ.get("REQUEST_METHOD", "GET").upper()
    raw_path = environ.get("PATH_INFO", "/") or "/"

    # Normalize path: strip query parameters and trailing slash
    path = raw_path.split("?")[0].rstrip("/") or "/"

    # 1. Handle CORS Preflight (OPTIONS)
    if method == "OPTIONS":
        return _build_response(
            start_response,
            "204 No Content",
            [
                ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),
                ("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With"),
            ],
            b"",
        )

    # 2. REST API: GET /api/health
    if path == "/api/health":
        body = json.dumps({
            "status": "healthy",
            "service": "MazeFlow AI",
            "version": "1.0.0",
            "algorithms": ["BFS", "DFS", "IDS", "A*"],
        }).encode("utf-8")
        return _build_response(
            start_response,
            "200 OK",
            [("Content-Type", "application/json; charset=utf-8")],
            body,
        )

    # 3. REST API: GET /api/mazes
    if path == "/api/mazes":
        from src.maze_agent.maze_library import get_predefined_mazes

        mazes = get_predefined_mazes()
        maze_list = [
            {
                "name": m.name,
                "rows": m.rows,
                "cols": m.cols,
                "walkable_count": m.walkable_cell_count,
                "start": list(m.start),
                "goal": list(m.goal),
            }
            for m in mazes.values()
        ]
        body = json.dumps({"count": len(maze_list), "mazes": maze_list}, indent=2).encode("utf-8")
        return _build_response(
            start_response,
            "200 OK",
            [("Content-Type", "application/json; charset=utf-8")],
            body,
        )

    # 4. REST API: POST /api/solve
    if path == "/api/solve":
        if method != "POST":
            return _build_response(
                start_response,
                "405 Method Not Allowed",
                [("Content-Type", "application/json")],
                b'{"error": "Method Not Allowed. Use POST."}',
            )

        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0) or 0)
        except (ValueError, TypeError):
            content_length = 0

        req_body = environ["wsgi.input"].read(content_length) if content_length > 0 else b""
        try:
            data = json.loads(req_body.decode("utf-8")) if req_body else {}
        except Exception as err:
            err_body = json.dumps({"error": f"Invalid JSON payload: {err}"}).encode("utf-8")
            return _build_response(
                start_response,
                "400 Bad Request",
                [("Content-Type", "application/json")],
                err_body,
            )

        algo_name = str(data.get("algorithm", "A*")).upper()
        preset_name = data.get("preset")
        maze_text = data.get("maze_text")

        from src.maze_agent.algorithms.astar import solve_astar
        from src.maze_agent.algorithms.bfs import solve_bfs
        from src.maze_agent.algorithms.dfs import solve_dfs
        from src.maze_agent.algorithms.ids import solve_ids
        from src.maze_agent.maze import Maze
        from src.maze_agent.maze_library import get_predefined_mazes

        algo_map = {
            "BFS": solve_bfs,
            "DFS": solve_dfs,
            "IDS": solve_ids,
            "A*": solve_astar,
            "ASTAR": solve_astar,
        }

        if algo_name not in algo_map:
            err_body = json.dumps({
                "error": f"Unknown algorithm '{algo_name}'. Supported: BFS, DFS, IDS, A*"
            }).encode("utf-8")
            return _build_response(
                start_response,
                "400 Bad Request",
                [("Content-Type", "application/json")],
                err_body,
            )

        try:
            if maze_text:
                maze = Maze.from_text(maze_text)
            elif preset_name:
                all_mazes = get_predefined_mazes()
                if preset_name not in all_mazes:
                    raise ValueError(f"Unknown preset maze '{preset_name}'")
                maze = all_mazes[preset_name]
            else:
                all_mazes = get_predefined_mazes()
                maze = all_mazes["small"]

            solver = algo_map[algo_name]
            result = solver(maze, record_trace=True)

            resp_data = {
                "algorithm": result.algorithm,
                "found": result.found,
                "path": result.path,
                "path_length": result.path_length,
                "nodes_expanded": result.nodes_expanded,
                "execution_time_seconds": result.execution_time_seconds,
                "status": result.status,
                "expanded_order": result.expanded_order,
                "depth_iterations": result.depth_iterations,
                "max_depth_reached": result.max_depth_reached,
            }
            body = json.dumps(resp_data).encode("utf-8")
            return _build_response(
                start_response,
                "200 OK",
                [("Content-Type", "application/json; charset=utf-8")],
                body,
            )
        except Exception as err:
            err_body = json.dumps({"error": str(err)}).encode("utf-8")
            return _build_response(
                start_response,
                "400 Bad Request",
                [("Content-Type", "application/json")],
                err_body,
            )

    # 5. Static File Serving from WEB_DIR
    rel_path = raw_path.lstrip("/")
    if not rel_path or rel_path == "index.html":
        target_file = WEB_DIR / "index.html"
    else:
        target_file = (WEB_DIR / rel_path).resolve()

    # Security check: Prohibit path traversal outside WEB_DIR
    try:
        target_file.relative_to(WEB_DIR)
    except ValueError:
        return _build_response(
            start_response,
            "403 Forbidden",
            [("Content-Type", "text/plain")],
            b"403 Forbidden: Path traversal prohibited.",
        )

    if target_file.is_file():
        if target_file.suffix == ".js":
            mime_type = "application/javascript"
        elif target_file.suffix == ".css":
            mime_type = "text/css"
        elif target_file.suffix == ".html":
            mime_type = "text/html"
        else:
            mime_type, _ = mimetypes.guess_type(str(target_file))
            if not mime_type:
                mime_type = "application/octet-stream"
            else:
                mime_type = "application/octet-stream"

        if mime_type.startswith("text/") or mime_type in (
            "application/javascript",
            "application/json",
        ):
            mime_type += "; charset=utf-8"

        try:
            content = target_file.read_bytes()
            return _build_response(
                start_response,
                "200 OK",
                [
                    ("Content-Type", mime_type),
                    ("Cache-Control", "public, max-age=3600"),
                ],
                content,
            )
        except Exception as err:
            err_body = f"500 Internal Server Error: {err}".encode("utf-8")
            return _build_response(
                start_response,
                "500 Internal Server Error",
                [("Content-Type", "text/plain")],
                err_body,
            )

    # 404 Fallback
    return _build_response(
        start_response,
        "404 Not Found",
        [("Content-Type", "text/plain")],
        b"404 Not Found",
    )


# Vercel entrypoint discovery variables (WSGI specification)
application = app
handler = app


def main() -> None:
    """Launch the interactive Tkinter desktop GUI when executed directly."""
    try:
        from src.maze_agent.gui.app import MazeSolverApp

        desktop_app = MazeSolverApp()
        desktop_app.mainloop()
    except (ImportError, Exception) as err:
        print(f"Tkinter desktop GUI unavailable ({err}).")
        print("Starting MazeFlow AI Web Server at http://localhost:8080 ...")
        from wsgiref.simple_server import make_server

        server = make_server("127.0.0.1", 8080, app)
        server.serve_forever()


if __name__ == "__main__":
    main()
