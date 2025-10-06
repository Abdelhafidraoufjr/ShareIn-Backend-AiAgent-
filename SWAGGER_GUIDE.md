# 🚀 AI Agent API - Documentation Swagger

## Démarrage Rapide

### 1. Installation
```bash
# Installer les dépendances
pip install -r requirements.txt

# OU utiliser le script automatique
python start_server.py
```

### 2. Lancement du serveur
```bash
# Méthode 1: Script automatique (recommandé)
python start_server.py

# Méthode 2: Démarrage manuel
python ai-agent.py
```

### 3. Accès à la documentation
Une fois le serveur démarré :

- **🌐 Interface Swagger UI** : http://localhost:5000/docs/
- **📄 Spécification OpenAPI** : http://localhost:5000/openapi.json
- **🔍 Health Check** : http://localhost:5000/health

## 📚 Utilisation de la Documentation

### Interface Swagger UI
La documentation interactive vous permet de :
- ✅ Explorer tous les endpoints disponibles
- 🧪 Tester les APIs directement depuis le navigateur
- 📋 Voir les modèles de données complets
- 🔐 Gérer l'authentification JWT
- 📥 Télécharger la spécification OpenAPI

### Workflow de Test Typique

1. **Health Check** : Testez `/health` pour vérifier que l'API fonctionne
2. **Inscription** : Créez un compte via `/auth/register`
3. **Connexion** : Récupérez un token JWT via `/auth/login`
4. **Autorisation** : Cliquez sur "Authorize" et entrez votre token
5. **Test d'endpoints** : Testez les endpoints protégés

## 🔧 Configuration

### Variables d'environnement (.env)
```env
# Azure OCR
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key

# Database
DATABASE_URL=sqlite:///ai_agent.db

# JWT
JWT_SECRET_KEY=your_secret_key
```

## 📖 Endpoints Principaux

### Authentification
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion
- `POST /auth/logout` - Déconnexion

### Traitement de Documents
- `POST /cin/process` - Traitement CIN
- `POST /permis/process` - Traitement Permis
- `POST /gris/process` - Traitement Carte Grise

### Analytics
- `GET /charts/overview` - Vue d'ensemble
- `GET /charts/essential` - Données essentielles
- `GET /charts/dashboard` - Dashboard complet

### Profil
- `GET /me` - Récupérer le profil
- `PUT /me` - Mettre à jour le profil

## 🧪 Test avec cURL

### Exemple de test complet
```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Inscription
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123","full_name":"Test User"}'

# 3. Connexion
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# 4. Test avec token (remplacez YOUR_TOKEN)
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/charts/overview
```

## 📱 Import Postman

Importez la collection Postman incluse :
1. Ouvrez Postman
2. Importez le fichier `postman_collection.json`
3. Configurez les variables d'environnement :
   - `baseUrl` : http://localhost:5000
   - `testEmail` : votre email de test
   - `testPassword` : votre mot de passe de test

## 🔍 Dépannage

### Problèmes Courants

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
```bash
# Changez le port dans ai-agent.py
app.run(debug=True, port=5001)
```

**"Swagger UI ne charge pas"**
- Vérifiez que le serveur est démarré
- Accédez à http://localhost:5000/docs/ (avec le slash final)
- Vérifiez la console pour les erreurs JavaScript

**"Token invalid"**
- Récupérez un nouveau token via `/auth/login`
- Vérifiez le format : `Bearer YOUR_TOKEN`

## 📊 Formats de Données

### Exemple CIN Response
```json
{
  "cin": "A123456",
  "identite": {
    "nom": {"fr": "DUPONT", "ar": "دوبون"},
    "prenom": {"fr": "JEAN", "ar": "جان"}
  },
  "naissance": {
    "date": "15.03.1990",
    "lieu": {"fr": "CASABLANCA", "ar": "الدار البيضاء"}
  },
  "sexe": "M",
  "validite": "15.03.2030"
}
```

## 🎯 Support

- 📧 Email : support@ai-agent.com
- 🐛 Issues : GitHub Issues
- 📖 Documentation : http://localhost:5000/docs/

---

**🎉 Votre documentation Swagger est maintenant opérationnelle !**