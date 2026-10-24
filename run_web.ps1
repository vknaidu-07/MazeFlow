# Launch MazeFlow AI Web Server
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "Starting MazeFlow AI Web Application" -ForegroundColor Green
Write-Host "URL: http://localhost:8080" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan

Start-Process "http://localhost:8080"
python -m http.server 8080 --directory web
