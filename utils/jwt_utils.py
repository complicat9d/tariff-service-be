import jwt
from datetime import timedelta

from utils.time_utils import utcnow
from config import settings


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])


def create_jwt_access_token(client_id: int) -> str:
    now = utcnow()
    data_to_encode = {
        "sub": str(client_id),
        "iat": now,
        "exp": now + timedelta(minutes=settings.TOKEN_EXPIRATION_DELTA),
    }
    encoded_refresh_jwt = jwt.encode(
        data_to_encode,
        settings.JWT_SECRET,
    )
    return encoded_refresh_jwt
