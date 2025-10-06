# Script PowerShell pour lancer les tests Locust
# Usage: .\run_locust.ps1 [web|headless] [users] [spawn-rate] [duration]

param(
    [string]$mode = "web",
    [int]$users = 50,
    [float]$spawnRate = 2,
    [string]$duration = "5m"
)

Write-Host "🐝 LANCEMENT DES TESTS LOCUST - AI AGENTS" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Vérifier si Locust est installé
try {
    locust --version | Out-Null
    Write-Host "✅ Locust détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Locust non installé" -ForegroundColor Red
    Write-Host "💡 Installation: pip install locust" -ForegroundColor Yellow
    exit 1
}

# Vérifier si le serveur Flask est accessible
Write-Host "🔍 Vérification du serveur Flask..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/openapi.json" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Serveur Flask accessible" -ForegroundColor Green
} catch {
    Write-Host "❌ Serveur Flask non accessible sur http://localhost:5000" -ForegroundColor Red
    Write-Host "💡 Démarrez le serveur: python ai-agent.py" -ForegroundColor Yellow
    exit 1
}

# Créer le dossier reports s'il n'existe pas
if (!(Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
    Write-Host "📁 Dossier reports créé" -ForegroundColor Cyan
}

# Configuration des paramètres
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$htmlReport = "reports/locust_report_$timestamp.html"
$csvReport = "reports/locust_data_$timestamp"

Write-Host ""
Write-Host "📊 Configuration du test:" -ForegroundColor Yellow
Write-Host "  Mode: $mode" -ForegroundColor White
Write-Host "  Utilisateurs: $users" -ForegroundColor White
Write-Host "  Taux de spawn: $spawnRate/sec" -ForegroundColor White
Write-Host "  Durée: $duration" -ForegroundColor White
Write-Host "  Rapport HTML: $htmlReport" -ForegroundColor White
Write-Host ""

# Construire la commande Locust
$locustCmd = "locust -f locustfile.py --host=http://localhost:5000"

if ($mode -eq "headless") {
    # Mode headless (sans interface web)
    $locustCmd += " --headless"
    $locustCmd += " --users $users"
    $locustCmd += " --spawn-rate $spawnRate"
    $locustCmd += " --run-time $duration"
    $locustCmd += " --html $htmlReport"
    $locustCmd += " --csv $csvReport"
    
    Write-Host "🚀 Lancement en mode headless..." -ForegroundColor Magenta
    Write-Host "⏱️ Durée estimée: $duration" -ForegroundColor Yellow
} else {
    # Mode web (avec interface)
    $locustCmd += " --web-host=0.0.0.0 --web-port=8089"
    
    Write-Host "🌐 Lancement en mode web..." -ForegroundColor Magenta
    Write-Host "🔗 Interface web: http://localhost:8089" -ForegroundColor Cyan
    Write-Host "💡 Configurez le test dans l'interface web" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📝 Commande exécutée:" -ForegroundColor Gray
Write-Host "$locustCmd" -ForegroundColor White
Write-Host ""

# Exécuter Locust
try {
    Invoke-Expression $locustCmd
} catch {
    Write-Host "❌ Erreur lors de l'exécution de Locust: $($_.Exception.Message)" -ForegroundColor Red
}

if ($mode -eq "headless") {
    Write-Host ""
    Write-Host "🏁 Test terminé!" -ForegroundColor Green
    Write-Host "📋 Rapport disponible: $htmlReport" -ForegroundColor Cyan
    Write-Host "📊 Données CSV: $csvReport.csv" -ForegroundColor Cyan
}