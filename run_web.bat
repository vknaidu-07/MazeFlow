@echo off
echo ===================================================
echo Starting MazeFlow AI Web Server at http://localhost:8080
echo ===================================================
start "" "http://localhost:8080"
python -m http.server 8080 --directory web
