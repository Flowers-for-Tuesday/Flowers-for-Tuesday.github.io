@echo off
echo Running git auto-push...

cd /d %~dp0

git add .
git commit -m "ud"
git push

echo Done!
pause
