import os
import json
import random
from locust import HttpUser, task, between, SequentialTaskSet
from io import BytesIO

class AuthenticatedUser(HttpUser):
    """Utilisateur authentifié pour tester les endpoints protégés"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Méthode appelée au démarrage de chaque utilisateur virtuel"""
        # Créer un utilisateur de test unique
        self.user_id = random.randint(1000, 9999)
        self.test_email = f"loadtest{self.user_id}@example.com"
        self.test_password = "password123"
        self.test_name = f"Load Test User {self.user_id}"
        
        # S'enregistrer puis se connecter
        self.register_and_login()
        
    def register_and_login(self):
        """Enregistrement et connexion de l'utilisateur de test"""
        # Tentative d'enregistrement
        register_data = {
            "email": self.test_email,
            "password": self.test_password,
            "full_name": self.test_name
        }
        
        with self.client.post("/auth/register", 
                             json=register_data, 
                             catch_response=True) as response:
            if response.status_code in [200, 201, 409]:  # 409 = utilisateur existe déjà
                print(f"✅ Enregistrement réussi/existant pour {self.test_email}")
            else:
                print(f"⚠️ Échec enregistrement: {response.status_code}")
        
        # Connexion
        login_data = {
            "email": self.test_email,
            "password": self.test_password
        }
        
        with self.client.post("/auth/login", 
                             json=login_data, 
                             catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.auth_token = data.get("token")
                    self.client.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    print(f"🔐 Connexion réussie pour {self.test_email}")
                except:
                    print("❌ Erreur lors de la récupération du token")
                    self.auth_token = None
            else:
                print(f"❌ Échec connexion: {response.status_code}")
                self.auth_token = None

    # =============================================================================
    # TESTS D'AUTHENTIFICATION (20% du trafic)
    # =============================================================================
    
    @task(5)
    def test_profile(self):
        """Test endpoint profil utilisateur"""
        if not self.auth_token:
            return
            
        with self.client.get("/me", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Profile failed: {response.status_code}")

    @task(2)
    def test_logout(self):
        """Test déconnexion puis reconnexion"""
        if not self.auth_token:
            return
            
        with self.client.post("/auth/logout", 
                            headers={"Authorization": f"Bearer {self.auth_token}"},
                            catch_response=True) as response:
            if response.status_code in [200, 204]:
                response.success()
                # Se reconnecter immédiatement
                self.register_and_login()
            else:
                response.failure(f"Logout failed: {response.status_code}")

    # =============================================================================
    # TESTS DES DOCUMENTS - CIN (30% du trafic)
    # =============================================================================
    
    @task(10)
    def test_get_all_cin(self):
        """Test récupération de tous les documents CIN"""
        if not self.auth_token:
            return
            
        with self.client.get("/cin/all", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"CIN all failed: {response.status_code}")

    @task(3)
    def test_process_cin(self):
        """Test traitement d'un document CIN (simulation)"""
        if not self.auth_token:
            return
            
        # Créer des fichiers factices pour le test
        fake_image = BytesIO(b"fake_image_content_for_testing")
        fake_image.name = "test_recto.jpg"
        
        fake_image2 = BytesIO(b"fake_image_content_for_testing_verso")
        fake_image2.name = "test_verso.jpg"
        
        files = {
            'recto': ('test_recto.jpg', fake_image, 'image/jpeg'),
            'verso': ('test_verso.jpg', fake_image2, 'image/jpeg')
        }
        
        with self.client.post("/cin/process", 
                            files=files,
                            headers={"Authorization": f"Bearer {self.auth_token}"},
                            catch_response=True) as response:
            if response.status_code in [200, 400, 500]:  # Accepter même les erreurs métier
                response.success()
            else:
                response.failure(f"CIN process failed: {response.status_code}")

    # =============================================================================
    # TESTS DES DOCUMENTS - PERMIS (25% du trafic)
    # =============================================================================
    
    @task(8)
    def test_get_all_permis(self):
        """Test récupération de tous les permis"""
        if not self.auth_token:
            return
            
        with self.client.get("/permis/all", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Permis all failed: {response.status_code}")

    @task(3)
    def test_process_permis(self):
        """Test traitement d'un permis de conduire"""
        if not self.auth_token:
            return
            
        fake_image = BytesIO(b"fake_permis_recto_content")
        fake_image.name = "permis_recto.jpg"
        
        fake_image2 = BytesIO(b"fake_permis_verso_content") 
        fake_image2.name = "permis_verso.jpg"
        
        files = {
            'recto': ('permis_recto.jpg', fake_image, 'image/jpeg'),
            'verso': ('permis_verso.jpg', fake_image2, 'image/jpeg')
        }
        
        with self.client.post("/permis/process", 
                            files=files,
                            headers={"Authorization": f"Bearer {self.auth_token}"},
                            catch_response=True) as response:
            if response.status_code in [200, 400, 500]:
                response.success()
            else:
                response.failure(f"Permis process failed: {response.status_code}")

    # =============================================================================
    # TESTS DES DOCUMENTS - CARTE GRISE (25% du trafic)
    # =============================================================================
    
    @task(8)
    def test_get_all_gris(self):
        """Test récupération de toutes les cartes grises"""
        if not self.auth_token:
            return
            
        with self.client.get("/gris/all", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gris all failed: {response.status_code}")

    @task(3)
    def test_process_gris(self):
        """Test traitement d'une carte grise"""
        if not self.auth_token:
            return
            
        fake_image = BytesIO(b"fake_gris_recto_content")
        fake_image.name = "gris_recto.jpg"
        
        fake_image2 = BytesIO(b"fake_gris_verso_content")
        fake_image2.name = "gris_verso.jpg"
        
        files = {
            'recto': ('gris_recto.jpg', fake_image, 'image/jpeg'),
            'verso': ('gris_verso.jpg', fake_image2, 'image/jpeg')
        }
        
        with self.client.post("/gris/process", 
                            files=files,
                            headers={"Authorization": f"Bearer {self.auth_token}"},
                            catch_response=True) as response:
            if response.status_code in [200, 400, 500]:
                response.success()
            else:
                response.failure(f"Gris process failed: {response.status_code}")

    @task(2)
    def test_gris_monthly_evolution(self):
        """Test évolution mensuelle des cartes grises"""
        if not self.auth_token:
            return
            
        with self.client.get("/gris/evolution-mensuel", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gris evolution failed: {response.status_code}")

    # =============================================================================
    # TESTS DES CHARTS/ANALYTICS (40% du trafic car très utilisés)
    # =============================================================================
    
    @task(12)
    def test_charts_overview(self):
        """Test aperçu général des graphiques"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/overview", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Charts overview failed: {response.status_code}")

    @task(8)
    def test_charts_dashboard(self):
        """Test dashboard principal"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/dashboard", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Charts dashboard failed: {response.status_code}")

    @task(6)
    def test_charts_gender_distribution(self):
        """Test distribution par genre"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/gender-distribution", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Gender distribution failed: {response.status_code}")

    @task(6)
    def test_charts_cities_distribution(self):
        """Test distribution par ville"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/cities-distribution", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Cities distribution failed: {response.status_code}")

    @task(5)
    def test_charts_license_categories(self):
        """Test catégories de permis"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/license-categories", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"License categories failed: {response.status_code}")

    @task(5)
    def test_charts_car_usage_types(self):
        """Test types d'usage des voitures"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/car-usage-types", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Car usage types failed: {response.status_code}")

    @task(4)
    def test_charts_monthly_stats(self):
        """Test statistiques mensuelles"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/monthly-stats", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Monthly stats failed: {response.status_code}")

    @task(4)
    def test_charts_daily_stats(self):
        """Test statistiques quotidiennes"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/daily-stats", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Daily stats failed: {response.status_code}")

    @task(3)
    def test_charts_essential(self):
        """Test données essentielles du dashboard"""
        if not self.auth_token:
            return
            
        with self.client.get("/charts/essential", 
                           headers={"Authorization": f"Bearer {self.auth_token}"},
                           catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Charts essential failed: {response.status_code}")


class PublicEndpointsUser(HttpUser):
    """Utilisateur pour tester les endpoints publics (sans authentification)"""
    wait_time = between(0.5, 2)
    weight = 2  # Moins d'utilisateurs pour les endpoints publics
    
    @task(10)
    def test_swagger_json(self):
        """Test accès à la spécification Swagger"""
        with self.client.get("/openapi.json", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Swagger JSON failed: {response.status_code}")

    @task(5)
    def test_swagger_ui(self):
        """Test accès à l'interface Swagger"""
        with self.client.get("/docs", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Swagger UI failed: {response.status_code}")

    @task(3)
    def test_docs_redirect(self):
        """Test redirection vers docs"""
        with self.client.get("/docs/", catch_response=True) as response:
            if response.status_code in [200, 301, 302]:
                response.success()
            else:
                response.failure(f"Docs redirect failed: {response.status_code}")


class AuthenticationFlowUser(SequentialTaskSet):
    """Flux séquentiel pour tester le processus complet d'authentification"""
    
    def on_start(self):
        self.user_id = random.randint(10000, 99999)
        self.test_email = f"seqtest{self.user_id}@example.com"
    
    @task
    def register_user(self):
        """Étape 1: Enregistrement"""
        register_data = {
            "email": self.test_email,
            "password": "sequentialtest123",
            "full_name": f"Sequential Test User {self.user_id}"
        }
        
        with self.client.post("/auth/register", json=register_data, catch_response=True) as response:
            if response.status_code in [200, 201, 409]:
                response.success()
            else:
                response.failure(f"Sequential register failed: {response.status_code}")
    
    @task  
    def login_user(self):
        """Étape 2: Connexion"""
        login_data = {
            "email": self.test_email,
            "password": "sequentialtest123"
        }
        
        with self.client.post("/auth/login", json=login_data, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.user.auth_token = data.get("token")
                    response.success()
                except:
                    response.failure("Token not received")
            else:
                response.failure(f"Sequential login failed: {response.status_code}")
    
    @task
    def access_profile(self):
        """Étape 3: Accès au profil"""
        if hasattr(self.user, 'auth_token') and self.user.auth_token:
            with self.client.get("/me", 
                               headers={"Authorization": f"Bearer {self.user.auth_token}"},
                               catch_response=True) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Sequential profile failed: {response.status_code}")
    
    @task
    def logout_user(self):
        """Étape 4: Déconnexion"""
        if hasattr(self.user, 'auth_token') and self.user.auth_token:
            with self.client.post("/auth/logout", 
                                headers={"Authorization": f"Bearer {self.user.auth_token}"},
                                catch_response=True) as response:
                if response.status_code in [200, 204]:
                    response.success()
                else:
                    response.failure(f"Sequential logout failed: {response.status_code}")


class SequentialFlowUser(HttpUser):
    """Utilisateur qui exécute le flux séquentiel"""
    wait_time = between(2, 5)
    weight = 1  # Moins d'utilisateurs pour les flux séquentiels
    tasks = [AuthenticationFlowUser]


# Configuration pour différents profils de test
class WebsiteUser(AuthenticatedUser):
    """Profil principal - utilisateur web standard"""
    weight = 8  # 80% des utilisateurs

class ApiUser(AuthenticatedUser):
    """Profil API - utilisateur qui utilise principalement les APIs"""
    weight = 2  # 20% des utilisateurs
    
    # Surcharger les poids pour ce profil (plus axé API)
    @task(15)
    def api_heavy_charts_overview(self):
        super().test_charts_overview()
    
    @task(10) 
    def api_heavy_get_all_cin(self):
        super().test_get_all_cin()
        
    @task(10)
    def api_heavy_get_all_permis(self):
        super().test_get_all_permis()
        
    @task(10)
    def api_heavy_get_all_gris(self):
        super().test_get_all_gris()
