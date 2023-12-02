from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import or_
from passlib.context import CryptContext
from jose import JWTError, jwt

from db import get_db_session, Session
from security import generate_jwt_token
from models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()
users_router = APIRouter()


def get_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        user_id = payload.get("user_id")
        username = payload.get("username")

        return User(user_id=user_id, username=username)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except (jwt.DecodeError, jwt.InvalidTokenError):
        raise HTTPException(status_code=401, detail="Invalid token")


@users_router.get("/users/info")
def get_user(user: User = Depends(get_user), session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    return {
        'users': user
    }


@users_router.get("/users/all")
def get_user(session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    return {
        'users': session.query(User).all()
    }


@users_router.delete('/users/delete')
def delete_user(user_id: int, session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    existing_user = session.query(User).filter(User.id==user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exists")

    session.delete(existing_user)
    session.commit()

    return {"message": "User was successfully deleted!"}


@users_router.post('/users/register')
def register(email: str, username: str, password: str, session: Session = Depends(get_db_session)):
    existing_user = session.query(User).filter(or_(User.email==email, User.username==username)).first()
    if existing_user:
        if existing_user.email==email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='email is occupied by another user')
        elif existing_user.username==username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='username is occupied by another user')

    new_user = User(email=email, username=username, hashed_password=pwd_context.hash(password))
    session.add(new_user)
    session.commit()

    return {"message": "User successfully registered!"}


@users_router.post('/users/login')
def login(email: str, password: str, session: Session = Depends(get_db_session)):
    user = session.query(User).filter(User.email == email).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid email or password')

    # Generate JWT token
    token = generate_jwt_token(user.id, user.username, user.email)
    return {'access_token': token}