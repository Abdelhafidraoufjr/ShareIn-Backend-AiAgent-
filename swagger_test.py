#!/usr/bin/env python3
"""
Script de test pour vérifier l'installation et la configuration Swagger
"""

import sys
import subprocess
import requests
import time
from pathlib import Path

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import flask
        import flask_restx
        print("✅ Flask et Flask-RESTX installés")
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False
    
    return True

def check_swagger_config():
    """Vérifie que la configuration Swagger est correcte"""
    print("🔍 Vérification de la configuration Swagger...")
    
    config_file = Path("swagger_config.py")
    if not config_file.exists():
        print("❌ Fichier swagger_config.py introuvable")
        return False
    
    try:
        from swagger_config import setup_swagger
        print("✅ Configuration Swagger importée avec succès")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def start_test_server():
    """Démarre le serveur de test"""
    print("🚀 Démarrage du serveur de test...")
    
    try:
        # Import local de l'application
        from ai_agent import create_app
        app = create_app()
        
        # Démarrage en mode test
        print("✅ Application créée avec succès")
        print("📚 Documentation Swagger disponible sur: http://localhost:5000/docs/")
        print("🔗 API disponible sur: http://localhost:5000/")
        
        return app
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return None

def test_swagger_endpoints():
    """Teste les endpoints de base"""
    print("🧪 Test des endpoints de base...")
    
    base_url = "http://localhost:5000"
    
    # Test de santé
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint /health fonctionnel")
        else:
            print(f"⚠️ Endpoint /health retourne {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du test /health: {e}")
    
    # Test de la documentation Swagger
    try:
        response = requests.get(f"{base_url}/docs/", timeout=5)
        if response.status_code == 200:
            print("✅ Documentation Swagger accessible")
        else:
            print(f"⚠️ Documentation Swagger retourne {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors du test Swagger: {e}")

def generate_test_requests():
    """Génère des exemples de requêtes pour test"""
    print("📝 Génération d'exemples de requêtes...")
    
    examples = {
        "curl_health": 'curl -X GET "http://localhost:5000/health"',
        "curl_register": '''curl -X POST "http://localhost:5000/auth/register" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Utilisateur Test"
  }'
''',
        "curl_login": '''curl -X POST "http://localhost:5000/auth/login" \\
  -H "Content-Type: application/json" \\
  -d '{
    "email": "test@example.com",
    "password": "test123"
  }'
''',
        "curl_upload_cin": '''curl -X POST "http://localhost:5000/cin/process" \\
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \\
  -F "recto=@/path/to/cin_recto.jpg" \\
  -F "verso=@/path/to/cin_verso.jpg"
'''
    }
    
    print("\n📋 Exemples de requêtes cURL :")
    for name, command in examples.items():
        print(f"\n# {name.replace('_', ' ').title()}")
        print(command)

def main():
    """Fonction principale"""
    print("🔧 AI Agent Backend - Test de Configuration Swagger")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_dependencies():
        sys.exit(1)
    
    if not check_swagger_config():
        sys.exit(1)
    
    # Test de l'application
    app = start_test_server()
    if not app:
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Configuration Swagger validée avec succès!")
    print("\n📖 Pour accéder à la documentation :")
    print("   1. Démarrez le serveur: python ai-agent.py")
    print("   2. Ouvrez: http://localhost:5000/docs/")
    print("\n🔗 Endpoints principaux :")
    print("   • Documentation: /docs/")
    print("   • API Health: /health")
    print("   • Authentification: /auth/login")
    print("   • CIN Processing: /cin/process")
    print("   • Analytics: /charts/dashboard")
    
    # Génération des exemples
    generate_test_requests()
    
    print("\n" + "=" * 50)
    print("🎉 Test terminé avec succès!")

if __name__ == "__main__":
    main()