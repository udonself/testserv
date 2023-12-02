from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(320))
    hashed_password = Column(String(60))


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)


class RoleOfUser(Base):
    __tablename__ = "user_roles" 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(f"{User.__tablename__}.id"))
    service_id = Column(Integer, ForeignKey(f"{Service.__tablename__}.id"))
    role_id = Column(Integer, ForeignKey(f"{Role.__tablename__}.id"))

