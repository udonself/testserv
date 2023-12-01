import os

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine, Column, Integer, String, or_ ,select, join, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import JWTError, jwt

from models import Base, User, Role, Service, RoleOfUser



load_dotenv()


engine = create_engine(os.getenv("DB_CONNECTION_STRING"))
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_db_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()


@app.get("/users/all")
def get_user(session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    return {
        'users': session.query(User).all()
    }


@app.delete('/users/delete')
def delete_user(user_id: int, session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    existing_user = session.query(User).filter(User.id==user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} does not exists")

    session.delete(existing_user)
    session.commit()

    return {"message": "User was successfully deleted!"}

# @app.post("/users/add")


@app.get("/roles/all")
def get_roles(session: Session = Depends(get_db_session)):
    # авторизация по jwt и определение роли пользователя
    return {
        'roles': session.query(Role).all()
    }


@app.get("/roles/users_roles")
def get_users_roles(session: Session = Depends(get_db_session)):
    stmt = (
        select(User.username, Service.name.label("service_name"), Role.name.label("role"))
        .select_from(
            join(RoleOfUser, User, RoleOfUser.user_id == User.id)
            .join(Service, RoleOfUser.service_id == Service.id)
            .join(Role, RoleOfUser.role_id == Role.id)
        )
    ) 
    result = session.execute(stmt)
    user_roles = result.fetchall()
    return {
        'users_roles': [{
            'username': username,
            'service': service,
            'role': role
        } for (username, service, role) in user_roles]
    }


@app.post('/users/register')
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


# @app.post('users/login')
# def login(email: str, username: str,)