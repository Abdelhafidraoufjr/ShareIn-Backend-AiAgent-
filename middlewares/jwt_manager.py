from datetime import datetime, timedelta
import jwt
from config.authentication_config import AuthConfig

JWT_SECRET = AuthConfig.SECRET_KEY
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRATION_HOURS = AuthConfig.TOKEN_EXPIRATION_HOURS

def create_access_token(user_id: int) -> str:
    now = datetime.utcnow()
    payload = {
        "sub": str(user_id),  # JWT standard => string
        "iat": int(now.timestamp()),  # ✅ timestamp entier
        "exp": int((now + timedelta(hours=TOKEN_EXPIRATION_HOURS)).timestamp()),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    # Compatibilité PyJWT < 2 (retourne bytes au lieu de str)
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"require": ["exp", "iat", "sub"]},  # on garde strict
        )
    except jwt.ExpiredSignatureError:
        raise Exception("Le token a expiré")
    except jwt.MissingRequiredClaimError as e:
        raise Exception(f"Claim manquant: {e.claim}")
    except jwt.InvalidTokenError as e:
        raise Exception(f"Token invalide: {str(e)}")

    user_id = payload.get("sub")
    if not user_id:
        raise Exception("Claim 'sub' introuvable dans le token")

    return int(user_id)
