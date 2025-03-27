@echo off
setlocal

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Installing...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-installer.exe

    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python installation failed. Exiting...
        exit /b 1
    ) else (
        echo Python installed successfully.
    )
)

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git not found. Installing...
    curl -L -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v2.44.0.windows.1/Git-2.44.0-64-bit.exe
    start /wait git-installer.exe /VERYSILENT /NORESTART
    del git-installer.exe

    git --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Git installation failed. Exiting...
        exit /b 1
    ) else (
        echo Git installed successfully.
    )
)

:: Install dependencies and run app
pip install -r src/cfg/requirements.txt
python src/main.py

endlocal
