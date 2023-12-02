from fastapi import FastAPI

from db import create_tables
from routers import users_router


create_tables()

app = FastAPI()

for router in (users_router,):
    app.include_router(router)

# @app.get("/roles/all")
# def get_roles(session: Session = Depends(get_db_session)):
#     # авторизация по jwt и определение роли пользователя
#     return {
#         'roles': session.query(Role).all()
#     }


# @app.get("/roles/users_roles")
# def get_users_roles(session: Session = Depends(get_db_session)):
#     stmt = (
#         select(User.username, Service.name.label("service_name"), Role.name.label("role"))
#         .select_from(
#             join(RoleOfUser, User, RoleOfUser.user_id == User.id)
#             .join(Service, RoleOfUser.service_id == Service.id)
#             .join(Role, RoleOfUser.role_id == Role.id)
#         )
#     ) 
#     result = session.execute(stmt)
#     user_roles = result.fetchall()
#     return {
#         'users_roles': [{
#             'username': username,
#             'service': service,
#             'role': role
#         } for (username, service, role) in user_roles]
#     }


# @app.post('users/login')
# def login(email: str, username: str,)