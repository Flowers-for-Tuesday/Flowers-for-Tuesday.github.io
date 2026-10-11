@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
python scripts\manage.py publish %*
set "publish_result=%errorlevel%"
pause
exit /b %publish_result%
