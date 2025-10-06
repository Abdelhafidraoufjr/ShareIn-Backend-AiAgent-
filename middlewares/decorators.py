from functools import wraps
from flask import request, jsonify
from auth.authentication_model import UserDB, SessionLocal
from middlewares.jwt_manager import verify_access_token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token manquant"}), 401

        token = auth_header.split(" ")[1]
        try:
            user_id = verify_access_token(token)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

        db = SessionLocal()
        user = db.query(UserDB).filter(UserDB.id == user_id).first()
        db.close()

        if not user:
            return jsonify({"error": "Utilisateur introuvable"}), 404

        return f(user, *args, **kwargs)
    return decorated
