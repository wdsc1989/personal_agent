@echo off
REM Script para inicializar Git e configurar repositório remoto

echo ============================================================
echo   INICIALIZANDO REPOSITORIO GIT
echo ============================================================
echo.

cd /d "%~dp0\.."

if exist .git (
    echo Repositorio Git ja inicializado.
    echo.
    git remote -v
    echo.
    goto :configurar
)

echo Inicializando repositorio Git...
git init

:configurar
echo.
echo Configurando repositorio remoto...
git remote remove origin 2>nul
git remote add origin https://github.com/wdsc1989/personal_agent.git

echo.
echo Adicionando todos os arquivos...
git add .

echo.
echo Criando commit inicial...
git commit -m "Initial commit: Agente Pessoal MVP"

echo.
echo ============================================================
echo   CONFIGURACAO CONCLUIDA!
echo ============================================================
echo.
echo Proximo passo:
echo   git push -u origin main
echo   OU
echo   git push -u origin master
echo.
echo Depois execute: scripts\preparar_deploy_local.bat
echo.
pause
