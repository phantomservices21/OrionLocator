@echo off
setlocal

:: Check if Git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed.
    echo You can install Git for Windows from git-scm.com.
    echo.

    choice /C YN /N /M "Would you like to open the Git installer page now? [y/n]: "
    if %errorlevel%==1 goto git_yes
    if %errorlevel%==2 goto git_no
)

goto check_python

:git_yes
echo Opening Git download page in your browser...
start https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe
goto check_python

:git_no
goto check_python

:check_python
:: Check if Python is installed.
python --version >nul 2>&1
if %errorlevel%==0 (
    pip install -r src/cfg/requirements.txt
    cls
    py src/main.py
    goto end
) else (
    echo Python is not installed.
    echo You can install version 3.13.2 from Python.org.
    echo.

    choice /C YN /N /M "Would you like to open the Python installer page now? [y/n]: "
    if %errorlevel%==1 goto python_yes
    if %errorlevel%==2 goto python_no
)

goto end

:python_yes
echo Opening Python.org in your browser...
start https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
goto end

:python_no
goto end

:end
endlocal
