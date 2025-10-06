# Tests de Charge avec Locust - AI Agents

## 🐝 Vue d'ensemble

Ce dossier contient une suite complète de tests de charge utilisant **Locust** pour l'API AI-Agents. Locust est un outil de test de charge moderne écrit en Python qui permet de simuler des milliers d'utilisateurs simultanés.

## 📋 Prérequis

### Installation de Locust

```bash
# Installation via pip
pip install locust

# Ou avec les dépendances complètes
pip install locust[all]

# Vérification
locust --version
```

### Serveur AI-Agents
Assurez-vous que le serveur Flask est démarré :
```bash
cd ../
python ai-agent.py
```

## 🗂️ Structure des fichiers

```
testing/
├── locustfile.py           # Tests Locust principaux
├── locust.conf             # Configuration Locust
├── run_locust.ps1          # Script PowerShell de lancement
├── reports/                # Rapports générés
└── README_LOCUST.md        # Cette documentation
```

## 🎯 Types d'utilisateurs simulés

### 1. **AuthenticatedUser** (80% du trafic)
- Utilisateurs authentifiés normaux
- Testent tous les endpoints protégés
- Pondération des tâches basée sur l'usage réel

### 2. **PublicEndpointsUser** (10% du trafic)
- Testent les endpoints publics (Swagger, docs)
- Pas d'authentification requise

### 3. **SequentialFlowUser** (10% du trafic)
- Simulent un parcours utilisateur complet
- Enregistrement → Connexion → Profil → Déconnexion

## 📊 Endpoints testés

### 🔐 Authentification
- `POST /auth/register` - Enregistrement
- `POST /auth/login` - Connexion
- `POST /auth/logout` - Déconnexion
- `GET /me` - Profil utilisateur

### 📄 Documents CIN
- `GET /cin/all` - Liste des CIN
- `POST /cin/process` - Traitement CIN

### 🚗 Permis de conduire
- `GET /permis/all` - Liste des permis
- `POST /permis/process` - Traitement permis

### 🚙 Cartes grises
- `GET /gris/all` - Liste des cartes grises
- `POST /gris/process` - Traitement carte grise
- `GET /gris/evolution-mensuel` - Évolution mensuelle

### 📈 Analytics/Charts
- `GET /charts/overview` - Aperçu général
- `GET /charts/dashboard` - Dashboard principal
- `GET /charts/gender-distribution` - Distribution par genre
- `GET /charts/cities-distribution` - Distribution par ville
- `GET /charts/license-categories` - Catégories de permis
- `GET /charts/car-usage-types` - Types d'usage véhicules
- `GET /charts/monthly-stats` - Statistiques mensuelles
- `GET /charts/daily-stats` - Statistiques quotidiennes
- `GET /charts/essential` - Données essentielles

### 📚 Documentation
- `GET /openapi.json` - Spécification OpenAPI
- `GET /docs` - Interface Swagger

## 🚀 Utilisation

### Mode Interface Web (Recommandé)

```powershell
# Lancement avec interface web
.\run_locust.ps1 web

# Ou directement
locust -f locustfile.py --host=http://localhost:5000
```

Puis ouvrir http://localhost:8089 dans le navigateur.

### Mode Headless (Automatique)

```powershell
# Test rapide (50 utilisateurs, 5 minutes)
.\run_locust.ps1 headless 50 2 5m

# Test intensif (200 utilisateurs, 10 minutes)
.\run_locust.ps1 headless 200 5 10m

# Test de stress (500 utilisateurs, 30 minutes)
.\run_locust.ps1 headless 500 10 30m
```

### Commandes Locust directes

```bash
# Mode web
locust -f locustfile.py --host=http://localhost:5000

# Mode headless
locust -f locustfile.py --host=http://localhost:5000 \
  --headless --users 100 --spawn-rate 3 --run-time 10m \
  --html reports/report.html --csv reports/data

# Avec configuration
locust --config=locust.conf
```

## 📈 Métriques collectées

### Métriques principales
- **Requests/sec** : Nombre de requêtes par seconde
- **Response Time** : Temps de réponse (min, max, moyenne, percentiles)
- **Failure Rate** : Taux d'échec des requêtes
- **Users** : Nombre d'utilisateurs virtuels actifs

### Métriques par endpoint
- Temps de réponse par route
- Taux de succès/échec
- Distribution des codes de statut
- Throughput par endpoint

## 📊 Rapports générés

### Rapport HTML
- Graphiques interactifs
- Statistiques détaillées
- Historique des performances
- Export possible

### Données CSV
- `*_stats.csv` - Statistiques par endpoint
- `*_stats_history.csv` - Historique des métriques
- `*_failures.csv` - Détails des échecs
- `*_exceptions.csv` - Exceptions rencontrées

## 🎮 Scénarios de test

### Test de Fumée (Smoke Test)
```powershell
.\run_locust.ps1 headless 5 1 2m
```

### Test de Charge Normale
```powershell
.\run_locust.ps1 headless 50 2 10m
```

### Test de Montée en Charge
```powershell
.\run_locust.ps1 headless 200 5 15m
```

### Test de Stress
```powershell
.\run_locust.ps1 headless 500 10 20m
```

### Test d'Endurance
```powershell
.\run_locust.ps1 headless 100 2 60m
```

## 🔧 Personnalisation

### Modifier les poids des tâches
Dans `locustfile.py`, ajustez les décorateurs `@task(weight)` :

```python
@task(10)  # Poids élevé = plus fréquent
def test_frequent_endpoint(self):
    pass

@task(1)   # Poids faible = moins fréquent  
def test_rare_endpoint(self):
    pass
```

### Ajouter de nouveaux endpoints

```python
@task(5)
def test_new_endpoint(self):
    if not self.auth_token:
        return
        
    with self.client.get("/new/endpoint", 
                       headers={"Authorization": f"Bearer {self.auth_token}"},
                       catch_response=True) as response:
        if response.status_code == 200:
            response.success()
        else:
            response.failure(f"New endpoint failed: {response.status_code}")
```

### Modifier les profils d'utilisateurs

```python
class HeavyUser(AuthenticatedUser):
    weight = 2  # 20% des utilisateurs
    
    @task(20)  # Plus lourd sur certains endpoints
    def heavy_task(self):
        super().test_charts_dashboard()
```

## 🔍 Surveillance et Debug

### Logs en temps réel
```bash
# Suivre les logs
tail -f locust.log

# Logs détaillés
locust -f locustfile.py --loglevel DEBUG
```

### Métriques système
Surveillez pendant les tests :
- CPU du serveur Flask
- Mémoire RAM utilisée
- Connexions base de données
- Latence réseau

## 📋 Bonnes pratiques

### Préparation
1. ✅ Serveur Flask démarré et stable
2. ✅ Base de données avec données de test
3. ✅ Ressources système suffisantes
4. ✅ Environnement isolé des utilisateurs réels

### Exécution
1. 🚀 Commencer par de petits tests (5-10 utilisateurs)
2. 📈 Augmenter progressivement la charge
3. ⏱️ Laisser suffisamment de temps pour stabilisation
4. 📊 Surveiller les métriques en temps réel

### Analyse
1. 📈 Analyser les tendances, pas juste les pics
2. 🔍 Identifier les endpoints les plus lents
3. ⚠️ Investiguer les taux d'erreur > 1%
4. 📝 Documenter les seuils de performance

## 🎯 Objectifs de performance

### Réponse acceptable
| Endpoint Type | Temps de réponse cible |
|---------------|------------------------|
| GET simple | < 200ms |
| GET complexe (charts) | < 500ms |
| POST simple | < 300ms |
| POST avec fichiers | < 2s |
| Authentification | < 400ms |

### Charge acceptable
- **50 utilisateurs simultanés** : Performance normale
- **100 utilisateurs simultanés** : Limite recommandée
- **200+ utilisateurs** : Test de stress

### Taux d'erreur
- **< 0.1%** : Excellent
- **< 1%** : Acceptable
- **> 5%** : Problématique

## 🚨 Dépannage

### Erreurs courantes

**"Connection refused"**
```bash
# Vérifier que le serveur Flask est démarré
curl http://localhost:5000/openapi.json
```

**"Auth token None"**
- Vérifier les credentials dans le code
- Vérifier l'endpoint de login

**"Too many open files"**
```bash
# Augmenter les limites système (Linux/Mac)
ulimit -n 4096
```

**Performances dégradées**
- Réduire le nombre d'utilisateurs
- Augmenter `wait_time`
- Vérifier les ressources système

---

*Tests de charge AI-Agents avec Locust - Documentation complète*