# Configuration environnement projet Kit App Template

Write-Host "=== Configuration environnement Kit App Template ===" -ForegroundColor Green

# Activation environnement virtuel Python 3.10
$venvPath = "D:\NVIDIA-Omniverse\kit-app-template\farm_env_py310"
$activateScript = "$venvPath\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "Activation environnement virtuel Python 3.10..." -ForegroundColor Cyan
    & $activateScript
} else {
    Write-Host "ERREUR: Environnement virtuel non trouvé à $venvPath" -ForegroundColor Red
    exit 1
}

# Variables d'environnement pour Farm
$env:FARM_URL = "http://localhost:8222"
$env:FARM_API_KEY = "change-me"

# Ajout du Farm local au PATH
$farmScriptsPath = "$venvPath\Scripts"
if ($env:PATH -notlike "*$farmScriptsPath*") {
    $env:PATH = "$farmScriptsPath;$env:PATH"
}

# Variables pour Omniverse Kit
$env:KIT_BUILD_PATH = "D:\NVIDIA-Omniverse\kit-app-template\_build\windows-x86_64\release"
$env:KIT_EXE = "$env:KIT_BUILD_PATH\kit\kit.exe"
$env:KIT_APP = "$env:KIT_BUILD_PATH\apps\pagerender.usd_compose.kit"

# Variables pour les dossiers de travail
$env:PROJECT_ROOT = "D:\NVIDIA-Omniverse\kit-app-template"
$env:USD_ASSETS = "D:\USD"
$env:RENDER_OUTPUT = "$env:PROJECT_ROOT\render_output"

Write-Host "✅ Environnement configuré:" -ForegroundColor Green
Write-Host "   - Python venv: farm_env_py310" -ForegroundColor Gray
Write-Host "   - Farm URL: $env:FARM_URL" -ForegroundColor Gray
Write-Host "   - Kit executable: $env:KIT_EXE" -ForegroundColor Gray
Write-Host "   - USD assets: $env:USD_ASSETS" -ForegroundColor Gray
Write-Host "   - Render output: $env:RENDER_OUTPUT" -ForegroundColor Gray
Write-Host ""
Write-Host "Commandes disponibles:" -ForegroundColor Yellow
Write-Host "   farm                              # Démarrer Farm queue" -ForegroundColor White
Write-Host "   python job_definition_upload.py   # Upload job definition" -ForegroundColor White
Write-Host "   python -c 'import sys; print(sys.executable)'  # Vérifier Python" -ForegroundColor White
Write-Host ""