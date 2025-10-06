# 🔐 Guide d'Authentification - AI Agent API

## Mise à Jour : Authentification Obligatoire

**Tous les endpoints de traitement et de récupération nécessitent maintenant une authentification JWT.**

## 📋 Endpoints avec Authentification Requise

### ✅ Authentification Non-Requise
- `GET /health` - Vérification de l'état du service
- `POST /auth/register` - Inscription
- `POST /auth/login` - Connexion  
- `POST /auth/logout` - Déconnexion

### 🔒 Authentification Requise (JWT Token)
- `GET /me` - Profil utilisateur
- `PUT /me` - Mise à jour du profil

#### Traitement de Documents
- `POST /cin/process` - Traitement CIN
- `GET /cin/all` - Récupération de toutes les CIN
- `POST /permis/process` - Traitement Permis
- `GET /permis/all` - Récupération de tous les permis
- `POST /gris/process` - Traitement Carte Grise
- `GET /gris/all` - Récupération de toutes les cartes grises
- `GET /gris/evolution-mensuel` - Évolution mensuelle

#### Analytics & Charts
- `GET /charts/overview` - Vue d'ensemble
- `GET /charts/gender-distribution` - Distribution par genre
- `GET /charts/cities-distribution` - Distribution par villes
- `GET /charts/license-categories` - Catégories de permis
- `GET /charts/car-usage-types` - Types d'usage véhicules
- `GET /charts/monthly-stats` - Statistiques mensuelles
- `GET /charts/daily-stats` - Statistiques quotidiennes
- `GET /charts/dashboard` - Dashboard complet
- `GET /charts/essential` - Dashboard essentiel

## 🚀 Workflow d'Authentification

### 1. Inscription
```bash
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "motdepasse123",
    "full_name": "Utilisateur Test"
  }'
```

**Réponse:**
```json
{
  "message": "User registered successfully"
}
```

### 2. Connexion et Récupération du Token
```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "motdepasse123"
  }'
```

**Réponse:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTg0MjE0NjJ9...."
}
```

### 3. Utilisation du Token pour les Endpoints Protégés

**⚠️ Important:** Tous les endpoints de traitement et analytics nécessitent maintenant le header `Authorization`

```bash
# Exemple: Traitement d'une CIN
curl -X POST http://localhost:5000/cin/process \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "recto=@/path/to/cin_recto.jpg" \
  -F "verso=@/path/to/cin_verso.jpg"

# Exemple: Récupération des analytics
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:5000/charts/overview
```

## 🔧 Configuration Swagger UI

### Test dans l'Interface Swagger

1. **Accédez à** : http://localhost:5000/docs/
2. **Cliquez sur "Authorize"** (bouton avec 🔒)
3. **Entrez votre token** : `Bearer YOUR_JWT_TOKEN`
4. **Cliquez "Authorize"** et fermez la popup
5. **Testez les endpoints** - l'authentification sera automatiquement incluse

### Exemple de Token dans Swagger
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2OTg0MjE0NjJ9....
```

## 📱 Configuration Postman

### Variables d'Environnement
```json
{
  "baseUrl": "http://localhost:5000",
  "testEmail": "user@example.com",
  "testPassword": "motdepasse123",
  "authToken": ""
}
```

### Script de Connexion Automatique
Dans l'endpoint "Login", ajoutez ce script dans l'onglet "Tests" :

```javascript
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("authToken", jsonData.token);
    console.log("Token saved:", jsonData.token);
}
```

## ❌ Gestion des Erreurs d'Authentification

### Token Manquant
```bash
curl http://localhost:5000/cin/all
```
**Réponse (401):**
```json
{
  "error": "Token required"
}
```

### Token Invalid/Expiré
```bash
curl -H "Authorization: Bearer invalid_token" \
  http://localhost:5000/cin/all
```
**Réponse (401):**
```json
{
  "error": "Token invalid"
}
```

### Format de Token Incorrect
```bash
curl -H "Authorization: invalid_token" \
  http://localhost:5000/cin/all
```
**Réponse (401):**
```json
{
  "error": "Token format invalid"
}
```

## 🧪 Script de Test Complet

```bash
#!/bin/bash

# Variables
BASE_URL="http://localhost:5000"
EMAIL="test@example.com"
PASSWORD="test123"

echo "🧪 Test complet de l'authentification AI Agent API"

# 1. Health Check (pas d'auth requise)
echo "1️⃣ Health Check..."
curl -s "$BASE_URL/health" | jq

# 2. Inscription
echo "2️⃣ Inscription..."
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\",\"full_name\":\"Test User\"}" | jq

# 3. Connexion et récupération du token
echo "3️⃣ Connexion..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}" | jq -r .token)

echo "Token reçu: ${TOKEN:0:50}..."

# 4. Test d'un endpoint protégé
echo "4️⃣ Test endpoint protégé..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/charts/overview" | jq

# 5. Test du profil
echo "5️⃣ Test profil utilisateur..."
curl -s -H "Authorization: Bearer $TOKEN" \
  "$BASE_URL/me" | jq

echo "✅ Tests terminés!"
```

## 🔄 Renouvellement du Token

Les tokens JWT ont une durée de vie limitée. Si vous recevez une erreur 401, reconnectez-vous :

```bash
# Récupérer un nouveau token
NEW_TOKEN=$(curl -s -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"motdepasse123"}' | jq -r .token)

# Utiliser le nouveau token
curl -H "Authorization: Bearer $NEW_TOKEN" \
  http://localhost:5000/charts/overview
```

## 📊 Exemple de Réponse avec Authentification Réussie

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/charts/overview
```

**Réponse (200):**
```json
{
  "total_cards": 1247,
  "identity_cards": 523,
  "driving_licenses": 384,
  "registration_cards": 340
}
```

---

**🎯 Votre API est maintenant entièrement sécurisée avec authentification JWT !**