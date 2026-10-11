@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
python scripts\manage.py preview --open
if errorlevel 1 pause
