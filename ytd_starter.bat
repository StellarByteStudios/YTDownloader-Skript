@echo off

:: Laden des Interpreters (für Virtuelle Umgebung)
set VENV_PYTHON="D:\Programmierung\Stuff\Youtube Downloader\YTDownloader-Skript\downloader.venv\Scripts\python.exe"

:: Pfad zum Skript
set SCRIPT_PATH="D:\Programmierung\Stuff\Youtube Downloader\YTDownloader-Skript\ytdownloader.py"

echo "%CD%"

:: Ausführung: Interpreter; Skript; Pfad von wo aus ausgeführt wird
%VENV_PYTHON% %SCRIPT_PATH% "%CD%"

pause