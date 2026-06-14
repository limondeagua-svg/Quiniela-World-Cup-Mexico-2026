@echo off
git add .
git commit -m "Actualizacion automatica"
git pull origin master --allow-unrelated-histories
git push -u origin master --force
echo.
echo ¡Listo! La quiniela ha sido forzada a GitHub.
pause