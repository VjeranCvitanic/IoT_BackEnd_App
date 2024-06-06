@echo off
:: Check for administrative privileges
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please right-click on the script and select "Run as administrator".
    pause
    exit /b
)

echo Building Docker image...
docker build -t my-fastapi-app .

if %errorlevel% neq 0 (
    echo Failed to build Docker image.
    pause
    exit /b
)

echo Running Docker container...
docker run -d -p 8000:8000 my-fastapi-app

if %errorlevel% neq 0 (
    echo Failed to run Docker container.
    pause
    exit /b
)

echo Docker container is running and FastAPI app should be accessible at http://localhost:8000
pause