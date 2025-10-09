import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.identity_card_routes import cin_bp
from routes.driving_license_routes import permis_bp
from routes.vehicle_registration_routes import gris_bp
from auth.authentication_routes import auth_bp
from charts.chart_routes import charts_bp
from middlewares.decorators import token_required
from swagger_configuration import setup_swagger
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")

def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    CORS(app, resources={r"/*": {"origins": CORS_ORIGIN}})
    
    requests_total = Counter(
    "requests_total", 
    "Total HTTP requests", 
    ["method", "endpoint"]
)

    @app.before_request
    def before_request():
        requests_total.labels(
        method=request.method,
        endpoint=request.path
    ).inc()

    
    
    # Configuration Swagger simple
    setup_swagger(app)

    app.register_blueprint(cin_bp, url_prefix="/cin")
    app.register_blueprint(permis_bp, url_prefix="/permis")
    app.register_blueprint(gris_bp, url_prefix="/gris")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(charts_bp, url_prefix="/charts")


    @app.route("/me")
    @token_required
    def profile(current_user):
        # Informations utilisateur de base
        user_data = {
            "email": current_user.email, 
            "full_name": current_user.full_name,
            "id": current_user.id
        }
        
        # Ajouter des statistiques d'activité (exemples statiques pour la démo)
        # Dans un vrai projet, ces données viendraient de la base de données
        user_data.update({
            "phone": getattr(current_user, 'phone', None),
            "address": getattr(current_user, 'address', None),
            "job_title": getattr(current_user, 'job_title', None),
            "department": getattr(current_user, 'department', None),
            "created_at": getattr(current_user, 'created_at', None),
            "last_login": getattr(current_user, 'last_login', None),
            "stats": {
                "total_cards_processed": 35,
                "identity_cards": 12,
                "driving_licenses": 8,
                "registration_cards": 15,
                "last_activity": "Il y a 2 heures"
            }
        })
        
        return user_data

    @app.route("/me", methods=["PUT"])
    @token_required
    def update_profile(current_user):
        from flask import request, jsonify
        
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({"error": "Aucune donnée fournie"}), 400
        
        # Mise à jour des champs autorisés
        if 'full_name' in data:
            current_user.full_name = data['full_name']
        
        # Pour l'instant, on simule la mise à jour des autres champs
        # Dans un vrai projet, il faudrait ajouter ces colonnes à la base de données
        
        try:
            # Sauvegarder en base (simulation)
            # session.commit()
            
            return jsonify({
                "message": "Profil mis à jour avec succès",
                "user": {
                    "email": current_user.email,
                    "full_name": current_user.full_name,
                    "id": current_user.id
                }
            })
        except Exception as e:
            return jsonify({"error": f"Erreur lors de la mise à jour: {str(e)}"}), 500

    @app.route("/health")
    def health_check():
        return {"status": "ok"}
    
    @app.route("/metrics")
    def metrics():
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
