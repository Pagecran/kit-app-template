@echo off
REM Configuration environnement projet Kit App Template

REM Activation environnement virtuel Python 3.10
call "D:\NVIDIA-Omniverse\kit-app-template\farm_env_py310\Scripts\activate.bat"

REM Variables d'environnement pour Farm
set FARM_URL=http://localhost:8222
set FARM_API_KEY=change-me

REM Ajout du Farm local au PATH
set PATH=D:\NVIDIA-Omniverse\kit-app-template\farm_env_py310\Scripts;%PATH%

REM Variables pour Omniverse Kit
set KIT_BUILD_PATH=D:\NVIDIA-Omniverse\kit-app-template\_build\windows-x86_64\release
set KIT_EXE=%KIT_BUILD_PATH%\kit\kit.exe
set KIT_APP=%KIT_BUILD_PATH%\apps\pagerender.usd_compose.kit

echo Environment configured:
echo - Python venv: farm_env_py310
echo - Farm URL: %FARM_URL%
echo - Kit executable: %KIT_EXE%
echo.
echo Usage:
echo   farm          - Start Farm queue
echo   python job_definition_upload.py hello-world.kit --farm-url %FARM_URL% --api-key %FARM_API_KEY%
echo.