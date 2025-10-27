from fastapi import APIRouter


user_rt = APIRouter(prefix="/users")


# @user_rt.get("/profile", tags=["Пользователи"])
# async def profile():
#     pass
#
#
# @user_rt.post("/auth/register", tags=["Пользователи"])
# async def register():
#     pass
#
#
# @user_rt.post("/auth/login", tags=["Пользователи"])
# async def login():
#     pass
#
#
# @user_rt.post("/auth/refresh", tags=["Пользователи"])
# async def refresh_token():
#     pass
