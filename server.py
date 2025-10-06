#!/usr/bin/env python3
"""
Script de démarrage et test pour l'API AI Agent avec Swagger
"""

import subprocess
import sys
import os
import time
import webbrowser

def install_dependencies():
    """Installe les dépendances nécessaires"""
    print("🔧 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def test_imports():
    """Teste les imports nécessaires"""
    print("🧪 Test des imports...")
    try:
        import flask
        import yaml
        from swagger_configuration import setup_swagger
        print("✅ Tous les imports sont OK")
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def check_files():
    """Vérifie que tous les fichiers nécessaires existent"""
    print("📁 Vérification des fichiers...")
    required_files = [
        "ai-agent.py",
        "swagger_config.py", 
        "openapi.yaml",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    
    print("✅ Tous les fichiers sont présents")
    return True

def start_server():
    """Démarre le serveur"""
    print("🚀 Démarrage du serveur...")
    print("📍 URL de l'API: http://localhost:5000")
    print("📚 Documentation Swagger: http://localhost:5000/docs/")
    print("🔗 Spécification OpenAPI: http://localhost:5000/openapi.json")
    print("\n⏳ Démarrage en cours...")
    
    # Attendre un peu puis ouvrir le navigateur
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open("http://localhost:5000/docs/")
            print("🌐 Documentation ouverte dans le navigateur")
        except:
            print("💡 Ouvrez manuellement: http://localhost:5000/docs/")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Démarrer l'application
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("application", "application.py")
        ai_agent = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ai_agent)
        app = ai_agent.create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False

def main():
    """Fonction principale"""
    print("🤖 AI Agent Backend - Démarrage avec Swagger")
    print("=" * 50)
    
    # Vérifications préliminaires
    if not check_files():
        sys.exit(1)
    
    # Installation des dépendances
    if not install_dependencies():
        print("💡 Essayez d'installer manuellement: pip install -r requirements.txt")
        sys.exit(1)
    
    # Test des imports
    if not test_imports():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Configuration validée - Démarrage du serveur...")
    print("=" * 50)
    
    # Démarrage du serveur
    start_server()

if __name__ == "__main__":
    main()