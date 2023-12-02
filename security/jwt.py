import os
from datetime import datetime, timedelta

from jose import jwt
from dotenv import load_dotenv


load_dotenv()


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = "HS256"


def generate_jwt_token(user_id: int, username: str, email: str) -> str:
    now = datetime.utcnow()
    expires = now + timedelta(days=365 * 10)
    encoded_payload = jwt.encode(
        {
            "user_id": user_id,
            "username": username,
            "email": email,
            "exp": expires
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_payload