@echo off

set SCRIPT_DIR=%~dp0
set VENV_DIR=%SCRIPT_DIR%downloader.venv-win
set SCRIPT_PATH=%SCRIPT_DIR%ytdownloader.py

if not exist "%VENV_DIR%" (
    echo Erstelle virtuelle Umgebung fuer Windows...
    python -m venv "%VENV_DIR%"
    "%VENV_DIR%\Scripts\pip.exe" install -r "%SCRIPT_DIR%requirements.txt"
)

echo "%CD%"

"%VENV_DIR%\Scripts\python.exe" "%SCRIPT_PATH%" "%CD%"

pause