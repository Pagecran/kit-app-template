# Script PowerShell pour arrêter et nettoyer Farm complètement
Write-Host "=== ARRET COMPLET ET NETTOYAGE FARM ===" -ForegroundColor Yellow

# 1. Arrêter tous les processus Farm
Write-Host "1. Identification et arrêt des processus Farm..." -ForegroundColor Cyan
$farmProcesses = Get-NetTCPConnection -LocalPort 8222 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
if ($farmProcesses) {
    foreach ($processId in $farmProcesses) {
        Write-Host "   Arrêt du processus Farm PID: $processId" -ForegroundColor Gray
        Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "   Aucun processus Farm détecté sur le port 8222" -ForegroundColor Gray
}

# 2. Vérification arrêt
Write-Host "2. Vérification arrêt..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
try {
    Invoke-WebRequest -Uri "http://localhost:8222/health" -TimeoutSec 3 -ErrorAction Stop | Out-Null
    Write-Host "   ❌ ATTENTION: Farm encore actif!" -ForegroundColor Red
    exit 1
} catch {
    Write-Host "   ✅ Farm arrêté" -ForegroundColor Green
}

# 3. Nettoyage complet
Write-Host "3. Nettoyage complet Farm..." -ForegroundColor Cyan
$dbPath = "C:\Users\p-andre\AppData\Local\nvidia\nv-svc-farm\task-management.db"
$jobDefsPath = "C:\Users\p-andre\AppData\Local\nvidia\nv-svc-farm\job-definitions"

if (Test-Path $dbPath) {
    Write-Host "   Suppression base de données tasks..." -ForegroundColor Gray
    Remove-Item $dbPath -Force -ErrorAction SilentlyContinue
}

if (Test-Path $jobDefsPath) {
    Write-Host "   Suppression job definitions..." -ForegroundColor Gray
    Remove-Item "$jobDefsPath\*" -Force -ErrorAction SilentlyContinue
}

Write-Host "✅ Nettoyage terminé" -ForegroundColor Green
Write-Host "Farm prêt pour redémarrage propre!" -ForegroundColor Yellow