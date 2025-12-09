@echo off
echo Running git auto-push...

:: 切换到脚本所在目录（可选，如果脚本就放在仓库根目录）
cd /d %~dp0

git add .
git commit -m "ud"
git push

echo Done!
pause
