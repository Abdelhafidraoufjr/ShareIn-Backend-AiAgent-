# AI Agent Backend API

## Description

API de traitement automatisé des documents d'identité marocains utilisant l'intelligence artificielle et l'OCR Azure. Cette API permet de traiter automatiquement :

- **Cartes d'Identité Nationales (CIN)** - Recto et verso
- **Permis de Conduire** - Extraction des informations de permis
- **Cartes Grises** - Documents d'immatriculation de véhicules

## 🚀 Démarrage Rapide

### Installation

```bash
# Cloner le projet
git clone <repository-url>
cd ai-agents

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API Azure
```

### Lancement

```bash
python ai-agent.py
```

L'API sera accessible sur `http://localhost:5000`

## 📚 Documentation Interactive

### Swagger UI
Une fois l'API lancée, accédez à la documentation interactive Swagger :

**URL :** `http://localhost:5000/docs/`

Cette interface vous permet de :
- Explorer tous les endpoints disponibles
- Tester les API directement depuis le navigateur
- Voir les modèles de données complets
- Comprendre les codes de réponse

## 🔐 Authentification

L'API utilise l'authentification JWT. Voici le workflow :

### 1. Inscription
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "motdepasse123",
  "full_name": "Nom Complet"
}
```

### 2. Connexion
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

**Réponse :**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Utilisation du Token
Pour tous les endpoints protégés, inclure le header :
```http
Authorization: Bearer <your_jwt_token>
```

## 📋 Endpoints Principaux

### Traitement des Documents

#### Carte d'Identité Nationale
```http
POST /cin/process
Content-Type: multipart/form-data
Authorization: Bearer <token>

# Fichiers requis :
# - recto: Image du recto de la CIN
# - verso: Image du verso de la CIN
```

#### Permis de Conduire
```http
POST /permis/process
Content-Type: multipart/form-data
Authorization: Bearer <token>

# Fichiers requis :
# - recto: Image du recto du permis
# - verso: Image du verso du permis (optionnel)
```

#### Carte Grise
```http
POST /gris/process
Content-Type: multipart/form-data
Authorization: Bearer <token>

# Fichiers requis :
# - recto: Image du recto de la carte grise
# - verso: Image du verso de la carte grise
```

### Récupération des Données

#### Toutes les CIN traitées
```http
GET /cin/all
Authorization: Bearer <token>
```

#### Tous les permis traités
```http
GET /permis/all
Authorization: Bearer <token>
```

#### Toutes les cartes grises traitées
```http
GET /gris/all
Authorization: Bearer <token>
```

### Analytics et Graphiques

#### Vue d'ensemble
```http
GET /charts/overview
Authorization: Bearer <token>
```

#### Distribution par genre
```http
GET /charts/gender-distribution
Authorization: Bearer <token>
```

#### Distribution par villes
```http
GET /charts/cities-distribution
Authorization: Bearer <token>
```

#### Données dashboard complet
```http
GET /charts/dashboard
Authorization: Bearer <token>
```

#### Données essentielles dashboard
```http
GET /charts/essential
Authorization: Bearer <token>
```

### Profil Utilisateur

#### Récupérer le profil
```http
GET /me
Authorization: Bearer <token>
```

#### Mettre à jour le profil
```http
PUT /me
Content-Type: application/json
Authorization: Bearer <token>

{
  "full_name": "Nouveau Nom",
  "phone": "+212600000000",
  "job_title": "Développeur"
}
```

## 📊 Modèles de Données

### CIN (Carte d'Identité Nationale)
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
  "adresse": {"fr": "123 RUE PRINCIPALE", "ar": "123 الشارع الرئيسي"},
  "sexe": "M",
  "validite": "15.03.2030",
  "parents": {
    "pere": {"fr": "PAUL DUPONT", "ar": "بول دوبون"},
    "mere": {"fr": "MARIE DUPONT", "ar": "ماري دوبون"}
  },
  "etat_civil": {
    "numero_etat_civil": "123/2024"
  }
}
```

### Permis de Conduire
```json
{
  "permis": {
    "numero_permis": "55/193059",
    "date_delivrance": "15.01.2020",
    "date_expiration": "15.01.2030",
    "categorie": "B"
  },
  "identite": {
    "nom": {"fr": "MARTIN", "ar": "مارتان"},
    "prenom": {"fr": "PIERRE", "ar": "بيير"}
  },
  "naissance": {
    "date": "20.05.1985",
    "lieu": {"fr": "RABAT", "ar": "الرباط"}
  }
}
```

### Carte Grise
```json
{
  "numero_matricule_marocain": {"numero": "1234 أ 56"},
  "immatriculation_anterieure": {"numero": "WW-123456"},
  "mise_en_circulation": {"date": "15.01.2020"},
  "mise_en_circulation_au_maroc": {"date": "15.01.2020"},
  "mutation": {"date": "15.01.2021"},
  "usage": {
    "type": "Particulier",
    "description": "Usage personnel"
  },
  "marque": "TOYOTA",
  "Type": "COROLLA",
  "Genre": "BERLINE",
  "type_carburant": "ESSENCE",
  "numero_chassis": "ABC123456789",
  "nombre_cylindres": 4,
  "puissance_fiscale": 8,
  "restriction": "AUCUNE",
  "identite": {
    "nom": {"fr": "ALAMI", "ar": "العلمي"},
    "prenom": {"fr": "MOHAMED", "ar": "محمد"}
  },
  "adresse": {"fr": "456 AVENUE HASSAN II", "ar": "456 شارع الحسن الثاني"},
  "valiadtion": "15.01.2025"
}
```

## 🔧 Configuration

### Variables d'Environnement (.env)
```env
# Azure OCR Configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your_azure_endpoint
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_azure_key

# Database Configuration
DATABASE_URL=sqlite:///ai_agent.db

# JWT Configuration
JWT_SECRET_KEY=your_secret_key

# OpenAI Configuration (si utilisé)
OPENAI_API_KEY=your_openai_key
```

## 🎯 Formats Acceptés

### Images
- **Formats :** JPG, JPEG, PNG, BMP, TIFF
- **Taille maximale :** 10MB par fichier
- **Résolution recommandée :** Minimum 300 DPI pour une meilleure précision OCR

### Données de Sortie
- **Format :** JSON structuré selon les modèles Pydantic
- **Validation :** Validation automatique des formats (dates, numéros, etc.)
- **Support multilingue :** Français et Arabe

## 🚨 Gestion d'Erreurs

### Codes de Statut HTTP
- **200** : Succès
- **201** : Créé avec succès
- **400** : Requête invalide (données manquantes/incorrectes)
- **401** : Non authentifié (token manquant/invalide)
- **500** : Erreur serveur

### Format des Erreurs
```json
{
  "error": "Description détaillée de l'erreur"
}
```

### Exemples d'Erreurs Courantes

#### Authentification requise
```json
{
  "error": "Token required"
}
```

#### Fichiers manquants
```json
{
  "error": "Veuillez uploader recto et verso"
}
```

#### Erreur de parsing
```json
{
  "error": "Erreur de parsing: CIN format invalid"
}
```

## 🧪 Tests

### Test avec cURL

#### Test de santé
```bash
curl -X GET http://localhost:5000/health
```

#### Upload CIN
```bash
curl -X POST http://localhost:5000/cin/process \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "recto=@/path/to/cin_recto.jpg" \
  -F "verso=@/path/to/cin_verso.jpg"
```

### Test avec Postman
1. Importer la collection depuis `/docs/` (génération automatique possible)
2. Configurer la variable d'environnement `{{baseUrl}}` = `http://localhost:5000`
3. Ajouter le token JWT dans l'onglet Authorization

## 🛡️ Sécurité

### Bonnes Pratiques Implémentées
- **JWT Tokens :** Authentification sécurisée avec expiration
- **Validation des données :** Modèles Pydantic avec validation stricte
- **CORS configuré :** Cross-Origin Resource Sharing approprié
- **Gestion des erreurs :** Messages d'erreur sécurisés
- **Upload sécurisé :** Validation des types de fichiers

### Recommandations Production
- Utiliser HTTPS en production
- Configurer un reverse proxy (Nginx)
- Utiliser une base de données PostgreSQL
- Mettre en place une limitation de taux (rate limiting)
- Logs et monitoring appropriés

## 📈 Performance

### Optimisations
- **OCR Azure :** Service cloud haute performance
- **Validation Pydantic :** Validation rapide et stricte
- **SQLAlchemy :** ORM optimisé avec connexions poolées
- **Cache :** Système de cache pour les réponses fréquentes

### Métriques Typiques
- **Traitement CIN :** 3-5 secondes (selon qualité image)
- **Traitement Permis :** 2-4 secondes
- **Traitement Carte Grise :** 4-6 secondes
- **APIs Analytics :** < 1 seconde

## 🤝 Support

### Issues Communes

1. **"ModuleNotFoundError"**
   - Vérifier l'installation : `pip install -r requirements.txt`

2. **"Azure Service Error"**
   - Vérifier les clés API Azure dans `.env`

3. **"Token Invalid"**
   - Récupérer un nouveau token via `/auth/login`

4. **"OCR Quality Poor"**
   - Utiliser des images haute résolution
   - Éviter les images floues ou mal éclairées

### Contact
- **Email :** support@ai-agent.com
- **Documentation :** http://localhost:5000/docs/
- **Issues :** GitHub Issues

---

## 📝 Historique des Versions

### v1.0.0
- ✅ Traitement CIN, Permis, Carte Grise
- ✅ Authentification JWT
- ✅ APIs Analytics/Dashboard
- ✅ Documentation Swagger complète
- ✅ Support multilingue FR/AR