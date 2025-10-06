"""
Configuration Swagger simple pour l'API AI Agent
"""
from flask import Flask, jsonify, render_template_string
import json

def setup_swagger(app: Flask):
    """Configure la documentation Swagger simple"""
    
    # Endpoint pour servir la spécification OpenAPI
    @app.route('/openapi.json')
    def openapi_spec():
        """Retourne la spécification OpenAPI en JSON"""
        try:
            with open('openapi.yaml', 'r', encoding='utf-8') as f:
                import yaml
                spec = yaml.safe_load(f)
                return jsonify(spec)
        except Exception as e:
            # Fallback avec spécification basique
            return jsonify({
                "openapi": "3.0.3",
                "info": {
                    "title": "AI Agent API",
                    "version": "1.0.0",
                    "description": "API pour le traitement automatisé des documents d'identité"
                },
                "servers": [{"url": "http://localhost:5000"}],
                "paths": {
                    "/health": {
                        "get": {
                            "summary": "Health Check",
                            "responses": {"200": {"description": "OK"}}
                        }
                    }
                }
            })
    
    # Interface Swagger UI simple
    @app.route('/docs/')
    @app.route('/docs')
    def swagger_ui():
        """Interface Swagger UI"""
        swagger_ui_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Agent API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css" />
    <style>
        html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
        *, *:before, *:after { box-sizing: inherit; }
        body { margin:0; background: #fafafa; }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null,
                tryItOutEnabled: true,
                supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                onComplete: function() {
                    console.log("Swagger UI loaded successfully");
                },
                onFailure: function(data) {
                    console.log("Failed to load API definition", data);
                }
            });
        };
    </script>
</body>
</html>'''
        return swagger_ui_html
    
    return app

    # Modèles pour l'authentification
    auth_register_model = api.model('AuthRegister', {
        'email': fields.String(required=True, description='Adresse email de l\'utilisateur'),
        'password': fields.String(required=True, description='Mot de passe'),
        'full_name': fields.String(required=False, description='Nom complet de l\'utilisateur')
    })

    auth_login_model = api.model('AuthLogin', {
        'email': fields.String(required=True, description='Adresse email'),
        'password': fields.String(required=True, description='Mot de passe')
    })

    auth_response_model = api.model('AuthResponse', {
        'token': fields.String(description='JWT Token d\'authentification')
    })

    # Modèles pour les données bilingues
    lang_text_model = api.model('LangText', {
        'fr': fields.String(required=True, description='Texte en français'),
        'ar': fields.String(required=True, description='Texte en arabe')
    })

    # Modèles pour CIN (Carte d'Identité Nationale)
    cin_identite_model = api.model('CINIdentite', {
        'nom': fields.Nested(lang_text_model, required=True),
        'prenom': fields.Nested(lang_text_model, required=True)
    })

    cin_naissance_model = api.model('CINNaissance', {
        'date': fields.String(required=True, description='Date de naissance (DD.MM.YYYY)'),
        'lieu': fields.Nested(lang_text_model, required=True)
    })

    cin_parent_model = api.model('CINParent', {
        'pere': fields.Nested(lang_text_model, required=True),
        'mere': fields.Nested(lang_text_model, required=True)
    })

    cin_etat_civil_model = api.model('CINEtatCivil', {
        'numero_etat_civil': fields.String(description='Numéro d\'état civil (XX/YYYY)')
    })

    cin_data_model = api.model('CINData', {
        'cin': fields.String(required=True, description='Numéro de la carte nationale'),
        'identite': fields.Nested(cin_identite_model, required=True),
        'naissance': fields.Nested(cin_naissance_model, required=True),
        'adresse': fields.Nested(lang_text_model, required=True, description='Adresse'),
        'sexe': fields.String(required=True, description='Sexe (M/F)', enum=['M', 'F']),
        'validite': fields.String(required=True, description='Date de validité (DD.MM.YYYY)'),
        'parents': fields.Nested(cin_parent_model, required=True),
        'etat_civil': fields.Nested(cin_etat_civil_model, required=True)
    })

    # Modèles pour Permis de Conduire
    permis_info_model = api.model('PermisInfo', {
        'numero_permis': fields.String(required=True, description='Numéro du permis (N/MMMMMM)'),
        'date_delivrance': fields.String(required=True, description='Date de délivrance (JJ.MM.AAAA)'),
        'date_expiration': fields.String(required=True, description='Date d\'expiration (JJ.MM.AAAA)'),
        'categorie': fields.String(required=True, description='Catégorie du permis', 
                                 enum=['A1', 'A', 'B', 'C', 'D', 'E(B)', 'E(C)', 'E(D)'])
    })

    permis_data_model = api.model('PermisData', {
        'permis': fields.Nested(permis_info_model, required=True),
        'identite': fields.Nested(cin_identite_model, required=True),
        'naissance': fields.Nested(cin_naissance_model, required=True)
    })

    # Modèles pour Carte Grise
    matricule_model = api.model('NumeroMatricule', {
        'numero': fields.String(required=True, description='Numéro de matricule (NNNN L NN)')
    })

    immatriculation_anterieure_model = api.model('ImmatriculationAnterieure', {
        'numero': fields.String(required=True, description='Numéro d\'immatriculation antérieure (WW-NNNNNN)')
    })

    date_model = api.model('Date', {
        'date': fields.String(required=True, description='Date (JJ.MM.AAAA)')
    })

    usage_model = api.model('Usage', {
        'type': fields.String(required=True, description='Type d\'usage', 
                            enum=['Particulier', 'Transport de marchandises', 'Transport en commun', 
                                'Location avec chauffeur', 'Location sans chauffeur']),
        'description': fields.String(required=True, description='Description de l\'usage')
    })

    gris_data_model = api.model('CartGrisData', {
        'numero_matricule_marocain': fields.Nested(matricule_model, required=True),
        'immatriculation_anterieure': fields.Nested(immatriculation_anterieure_model, required=True),
        'mise_en_circulation': fields.Nested(date_model, required=True),
        'mise_en_circulation_au_maroc': fields.Nested(date_model, required=True),
        'mutation': fields.Nested(date_model, required=True),
        'usage': fields.Nested(usage_model, required=True),
        'marque': fields.String(required=True, description='Marque du véhicule'),
        'Type': fields.String(required=True, description='Type du véhicule'),
        'Genre': fields.String(required=True, description='Genre du véhicule'),
        'type_carburant': fields.String(required=True, description='Type de carburant'),
        'numero_chassis': fields.String(required=True, description='Numéro de châssis'),
        'nombre_cylindres': fields.Integer(required=True, description='Nombre de cylindres'),
        'puissance_fiscale': fields.Integer(required=True, description='Puissance fiscale en CV'),
        'restriction': fields.String(required=True, description='Restrictions éventuelles'),
        'identite': fields.Nested(cin_identite_model, required=True),
        'adresse': fields.Nested(lang_text_model, required=True),
        'valiadtion': fields.String(required=True, description='Date de validité (JJ.MM.AAAA)')
    })

    # Modèles pour les graphiques et statistiques
    chart_overview_model = api.model('ChartOverview', {
        'total_cards': fields.Integer(description='Nombre total de cartes traitées'),
        'identity_cards': fields.Integer(description='Nombre de cartes d\'identité'),
        'driving_licenses': fields.Integer(description='Nombre de permis de conduire'),
        'registration_cards': fields.Integer(description='Nombre de cartes grises')
    })

    gender_distribution_model = api.model('GenderDistribution', {
        'M': fields.Integer(description='Nombre d\'hommes'),
        'F': fields.Integer(description='Nombre de femmes')
    })

    cities_distribution_model = api.model('CitiesDistribution', {
        'cities': fields.List(fields.Raw, description='Liste des villes avec leurs statistiques')
    })

    # Modèle de profil utilisateur
    user_profile_model = api.model('UserProfile', {
        'email': fields.String(description='Email de l\'utilisateur'),
        'full_name': fields.String(description='Nom complet'),
        'id': fields.Integer(description='ID utilisateur'),
        'phone': fields.String(description='Numéro de téléphone'),
        'address': fields.String(description='Adresse'),
        'job_title': fields.String(description='Titre du poste'),
        'department': fields.String(description='Département'),
        'created_at': fields.String(description='Date de création du compte'),
        'last_login': fields.String(description='Dernière connexion'),
        'stats': fields.Raw(description='Statistiques d\'activité')
    })

    # Modèles d'erreur
    error_model = api.model('Error', {
        'error': fields.String(required=True, description='Message d\'erreur')
    })

    success_model = api.model('Success', {
        'message': fields.String(required=True, description='Message de succès')
    })

    # Configuration des espaces de noms
    auth_ns = api.namespace('auth', description='Authentification et gestion des utilisateurs')
    cin_ns = api.namespace('cin', description='Traitement des cartes d\'identité nationales')
    permis_ns = api.namespace('permis', description='Traitement des permis de conduire')
    gris_ns = api.namespace('gris', description='Traitement des cartes grises')
    charts_ns = api.namespace('charts', description='Données analytiques et graphiques')
    profile_ns = api.namespace('profile', description='Gestion du profil utilisateur')

    # Documentation des endpoints d'authentification
    @auth_ns.route('/register')
    class AuthRegister(Resource):
        @auth_ns.expect(auth_register_model)
        @auth_ns.marshal_with(success_model, code=201)
        @auth_ns.response(400, 'Données invalides', error_model)
        def post(self):
            """Inscription d'un nouvel utilisateur"""
            pass

    @auth_ns.route('/login')
    class AuthLogin(Resource):
        @auth_ns.expect(auth_login_model)
        @auth_ns.marshal_with(auth_response_model, code=200)
        @auth_ns.response(401, 'Identifiants invalides', error_model)
        def post(self):
            """Connexion utilisateur"""
            pass

    @auth_ns.route('/logout')
    class AuthLogout(Resource):
        @auth_ns.marshal_with(success_model, code=200)
        def post(self):
            """Déconnexion utilisateur"""
            pass

    # Documentation des endpoints CIN
    upload_parser = api.parser()
    upload_parser.add_argument('recto', location='files', type=FileStorage, required=True, help='Image du recto de la carte')
    upload_parser.add_argument('verso', location='files', type=FileStorage, required=True, help='Image du verso de la carte')

    @cin_ns.route('/process')
    class CINProcess(Resource):
        @cin_ns.expect(upload_parser)
        @cin_ns.marshal_with(cin_data_model, code=200)
        @cin_ns.response(400, 'Fichiers manquants ou invalides', error_model)
        @cin_ns.response(500, 'Erreur de traitement', error_model)
        def post(self):
            """Traitement d'une carte d'identité nationale (recto + verso)"""
            pass

    @cin_ns.route('/all')
    class CINList(Resource):
        @cin_ns.marshal_list_with(cin_data_model, code=200)
        @cin_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Récupération de toutes les cartes d'identité traitées"""
            pass

    # Documentation des endpoints Permis
    permis_upload_parser = api.parser()
    permis_upload_parser.add_argument('recto', location='files', type=FileStorage, required=True, help='Image du recto du permis')
    permis_upload_parser.add_argument('verso', location='files', type=FileStorage, required=False, help='Image du verso du permis')

    @permis_ns.route('/process')
    class PermisProcess(Resource):
        @permis_ns.expect(permis_upload_parser)
        @permis_ns.marshal_with(permis_data_model, code=200)
        @permis_ns.response(400, 'Fichiers manquants ou invalides', error_model)
        @permis_ns.response(500, 'Erreur de traitement', error_model)
        def post(self):
            """Traitement d'un permis de conduire"""
            pass

    @permis_ns.route('/all')
    class PermisList(Resource):
        @permis_ns.marshal_list_with(permis_data_model, code=200)
        @permis_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Récupération de tous les permis de conduire traités"""
            pass

    # Documentation des endpoints Carte Grise
    @gris_ns.route('/process')
    class GrisProcess(Resource):
        @gris_ns.expect(upload_parser)
        @gris_ns.marshal_with(gris_data_model, code=200)
        @gris_ns.response(400, 'Fichiers manquants ou invalides', error_model)
        @gris_ns.response(500, 'Erreur de traitement', error_model)
        def post(self):
            """Traitement d'une carte grise (recto + verso)"""
            pass

    @gris_ns.route('/all')
    class GrisList(Resource):
        @gris_ns.marshal_list_with(gris_data_model, code=200)
        @gris_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Récupération de toutes les cartes grises traitées"""
            pass

    @gris_ns.route('/evolution-mensuel')
    class GrisEvolution(Resource):
        @gris_ns.response(200, 'Évolution mensuelle des immatriculations')
        @gris_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Évolution mensuelle des premières immatriculations"""
            pass

    # Documentation des endpoints Charts
    @charts_ns.route('/overview')
    class ChartsOverview(Resource):
        @charts_ns.marshal_with(chart_overview_model, code=200)
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Aperçu général des cartes traitées"""
            pass

    @charts_ns.route('/gender-distribution')
    class ChartsGender(Resource):
        @charts_ns.marshal_with(gender_distribution_model, code=200)
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Distribution par genre"""
            pass

    @charts_ns.route('/cities-distribution')
    class ChartsCities(Resource):
        @charts_ns.marshal_with(cities_distribution_model, code=200)
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Distribution par villes"""
            pass

    @charts_ns.route('/license-categories')
    class ChartsLicenseCategories(Resource):
        @charts_ns.response(200, 'Catégories de permis')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Distribution des catégories de permis"""
            pass

    @charts_ns.route('/car-usage-types')
    class ChartsCarUsage(Resource):
        @charts_ns.response(200, 'Types d\'usage des véhicules')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Distribution des types d'usage des véhicules"""
            pass

    @charts_ns.route('/monthly-stats')
    class ChartsMonthlyStats(Resource):
        @charts_ns.response(200, 'Statistiques mensuelles')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Statistiques de traitement mensuelles"""
            pass

    @charts_ns.route('/daily-stats')
    class ChartsDailyStats(Resource):
        @charts_ns.response(200, 'Statistiques quotidiennes')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Statistiques de traitement quotidiennes"""
            pass

    @charts_ns.route('/dashboard')
    class ChartsDashboard(Resource):
        @charts_ns.response(200, 'Données complètes du dashboard')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Toutes les données nécessaires pour le dashboard"""
            pass

    @charts_ns.route('/essential')
    class ChartsEssential(Resource):
        @charts_ns.response(200, 'Données essentielles du dashboard')
        @charts_ns.response(401, 'Non authentifié', error_model)
        @charts_ns.response(500, 'Erreur serveur', error_model)
        def get(self):
            """Données essentielles et fiables pour le dashboard"""
            pass

    # Documentation des endpoints de profil
    profile_update_model = api.model('ProfileUpdate', {
        'full_name': fields.String(description='Nom complet'),
        'phone': fields.String(description='Numéro de téléphone'),
        'address': fields.String(description='Adresse'),
        'job_title': fields.String(description='Titre du poste'),
        'department': fields.String(description='Département')
    })

    @profile_ns.route('/me')
    class ProfileMe(Resource):
        @profile_ns.marshal_with(user_profile_model, code=200)
        @profile_ns.response(401, 'Non authentifié', error_model)
        def get(self):
            """Récupération du profil utilisateur actuel"""
            pass

        @profile_ns.expect(profile_update_model)
        @profile_ns.marshal_with(success_model, code=200)
        @profile_ns.response(400, 'Données invalides', error_model)
        @profile_ns.response(401, 'Non authentifié', error_model)
        @profile_ns.response(500, 'Erreur serveur', error_model)
        def put(self):
            """Mise à jour du profil utilisateur"""
            pass

    # Endpoint de santé
    health_ns = api.namespace('health', description='Vérification de l\'état du service')
    
    @health_ns.route('/health')
    class HealthCheck(Resource):
        @health_ns.response(200, 'Service opérationnel')
        def get(self):
            """Vérification de l'état du service"""
            pass

    return api