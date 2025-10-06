from flask import Blueprint, request, jsonify
from auth.authentication_model import UserDB
import jwt
from datetime import datetime, timedelta
from utils.config import Config
import bcrypt
from auth.authentication_model import SessionLocal
from middlewares.jwt_manager import create_access_token, JWT_SECRET, JWT_ALGORITHM

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    pwd   = data.get("password")
    full_name = data.get("full_name")

    if not email or not pwd:
        return jsonify({"error": "Email and password required"}), 400

    session = SessionLocal()
    try:
        existing = session.query(UserDB).filter_by(email=email).first()
        if existing:
            return jsonify({"error": "Email already registered"}), 400

        salt   = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pwd.encode(), salt).decode()

        new_user = UserDB(email=email, hashed_password=hashed, full_name=full_name)
        session.add(new_user)
        session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    pwd   = data.get("password")

    if not email or not pwd:
        return jsonify({"error": "Email and password required"}), 400

    session = SessionLocal()
    try:
        user = session.query(UserDB).filter_by(email=email).first()
        if not user or not user.verify_password(pwd):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(user.id)

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()

@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logged out (client should discard token)"}), 200

@auth_bp.route("/auth0-exchange", methods=["POST"])
def auth0_exchange():
    """Échange un token Auth0 contre un token backend local"""
    try:
        data = request.get_json() or {}
        auth0_payload = request.current_user
        
        email = data.get('email') or auth0_payload.get('email')
        name = data.get('name') or auth0_payload.get('name')
        picture = data.get('picture')
        sub = data.get('sub') or auth0_payload.get('sub')
        
        if not email:
            return jsonify({'error': 'Email requis'}), 400
        
        session = SessionLocal()
        try:
            # Chercher l'utilisateur existant
            user = session.query(UserDB).filter_by(email=email).first()
            
            if user:
                # Mettre à jour avec les infos Auth0
                user.full_name = name or user.full_name
                user.auth0_sub = sub
                user.picture = picture
                user.last_login = datetime.utcnow()
            else:
                # Créer un nouvel utilisateur
                user = UserDB(
                    email=email,
                    full_name=name or 'Auth0 User',
                    password_hash='',  # Pas de mot de passe pour Auth0
                    auth0_sub=sub,
                    picture=picture
                )
                session.add(user)
            
            session.commit()
            
            # Créer un token backend
            token = create_access_token(user_id=user.id, email=user.email)
            
            return jsonify({
                'token': token,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'picture': user.picture,
                    'auth_type': 'auth0'
                }
            })
            
        finally:
            session.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500



     


    
