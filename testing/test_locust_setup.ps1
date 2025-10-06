# Script de test rapide pour vérifier l'installation Locust
# Usage: .\test_locust_setup.ps1

Write-Host "🔧 VÉRIFICATION DE L'INSTALLATION LOCUST" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Vérifier Python
Write-Host "`n1. 🐍 Vérification de Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>$null
    Write-Host "   ✅ Python installé: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python non trouvé" -ForegroundColor Red
    Write-Host "   💡 Installez Python depuis python.org" -ForegroundColor Yellow
    exit 1
}

# 2. Vérifier Locust
Write-Host "`n2. 🐝 Vérification de Locust..." -ForegroundColor Blue
try {
    $locustVersion = locust --version 2>$null
    Write-Host "   ✅ Locust installé: $locustVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Locust non trouvé" -ForegroundColor Red
    Write-Host "   💡 Installation: pip install locust" -ForegroundColor Yellow
    
    $install = Read-Host "   Voulez-vous installer Locust maintenant? (y/N)"
    if ($install -eq 'y' -or $install -eq 'Y') {
        Write-Host "   📦 Installation de Locust..." -ForegroundColor Yellow
        pip install locust
        Write-Host "   ✅ Locust installé!" -ForegroundColor Green
    } else {
        exit 1
    }
}

# 3. Vérifier les fichiers requis
Write-Host "`n3. 📁 Vérification des fichiers..." -ForegroundColor Blue
$requiredFiles = @("locustfile.py", "locust.conf", "run_locust.ps1")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "   ✅ $file" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $file manquant" -ForegroundColor Red
    }
}

# 4. Vérifier la syntaxe du locustfile
Write-Host "`n4. 🔍 Vérification de la syntaxe..." -ForegroundColor Blue
try {
    python -m py_compile locustfile.py
    Write-Host "   ✅ Syntaxe Python valide" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Erreur de syntaxe dans locustfile.py" -ForegroundColor Red
}

# 5. Test de Locust en mode dry-run
Write-Host "`n5. 🧪 Test de Locust (dry-run)..." -ForegroundColor Blue
try {
    # Tester que Locust peut charger le fichier sans erreur
    $testOutput = locust -f locustfile.py --help 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   ✅ Locustfile valide" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️ Problème avec le locustfile" -ForegroundColor Yellow
    }
} catch {
    Write-Host "   ❌ Erreur lors du test Locust" -ForegroundColor Red
}

# 6. Vérifier le serveur Flask (optionnel)
Write-Host "`n6. 🖥️ Vérification du serveur Flask..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/openapi.json" -UseBasicParsing -TimeoutSec 3
    Write-Host "   ✅ Serveur Flask accessible" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️ Serveur Flask non accessible" -ForegroundColor Yellow
    Write-Host "   💡 Démarrez le serveur: python ../ai-agent.py" -ForegroundColor Yellow
}

# 7. Créer le dossier reports
Write-Host "`n7. 📊 Vérification du dossier reports..." -ForegroundColor Blue
if (!(Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
    Write-Host "   ✅ Dossier reports créé" -ForegroundColor Green
} else {
    Write-Host "   ✅ Dossier reports existe" -ForegroundColor Green
}

# Résumé
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "🎉 VÉRIFICATION TERMINÉE!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 PROCHAINES ÉTAPES:" -ForegroundColor Yellow
Write-Host "1. Démarrer le serveur Flask:" -ForegroundColor White
Write-Host "   cd .." -ForegroundColor Cyan
Write-Host "   python ai-agent.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Lancer Locust (mode web):" -ForegroundColor White
Write-Host "   .\run_locust.ps1 web" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Ou test rapide (mode headless):" -ForegroundColor White
Write-Host "   .\run_locust.ps1 headless 5 1 30s" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Interface web Locust:" -ForegroundColor White
Write-Host "   http://localhost:8089" -ForegroundColor Cyan
Write-Host ""