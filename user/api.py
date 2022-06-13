from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException, status
from pydantic import EmailStr
from user.depends import get_current_user
from asyncpg.exceptions import UniqueViolationError
from .services import save_ava, delete_ava
from .security import hash_password, verify_password, create_access_token
from . import models as m
from . import schemas as s


user_router = APIRouter(tags=['user'])


@user_router.patch("/name", response_model=s.User)
async def update_username(new_name: str, user: m.User = Depends(get_current_user)):
    user.name = new_name
    return await user.update()


@user_router.patch("/email", response_model=s.User)
async def update_email(new_email: EmailStr, user: m.User = Depends(get_current_user)):
    if await m.User.objects.get_or_none(email=new_email) == None:
        user.email = new_email
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The email is occupied by another user")
    return await user.update()


@user_router.patch("/prefix", response_model=s.User)
async def update_prefix(new_prefix: str, user: m.User = Depends(get_current_user)):
    if await m.User.objects.get_or_none(prefix=new_prefix) == None:
        user.prefix = new_prefix
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The username is occupied by another user")
    return await user.update()


@user_router.post("/avatar", response_model=s.User)
async def create_avatar(
        back_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        user: m.User = Depends(get_current_user)
):
    return await save_ava(user, file, back_tasks)


@user_router.delete("/avatar")
async def delete_avatar(
        user: m.User = Depends(get_current_user)
):
    return delete_ava(user.ava)


@user_router.patch("/password", response_model=s.User)
async def update_password(old_password: str, new_password: str, user: m.User = Depends(get_current_user)):
    if verify_password(old_password, user.password):
        user.password = str(hash_password(new_password))
        return await user.update()
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")


@user_router.delete("/delete")
async def delete_account(password: str, user: m.User = Depends(get_current_user)):
    if verify_password(password, user.password):
        await m.User.objects.delete(id=user.id)
        return {"message": 'Successfully deleted'}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")


@user_router.post("/signup", response_model=s.UserWithToken)
async def create_user(user: s.UserCreate):
    user.password = str(hash_password(user.password))
    try:
        user = await m.User.objects.create(**user.dict(exclude={"password2"}))
    except UniqueViolationError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return s.UserWithToken(
        **user.dict(),
        token=s.Token(
            access_token=create_access_token({"sub": user.email}),
            token_type="Bearer"
        )
    )


@user_router.post("/auth", response_model=s.UserWithToken)
async def login(login: s.UserLogin):
    user = None
    if login.prefix:
        user = await m.User.objects.get_or_none(prefix=login.prefix)
    elif login.email:
        user = await m.User.objects.get_or_none(email=login.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    elif not verify_password(login.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    return s.UserWithToken(
        **user.dict(),
        token=s.Token(
            access_token=create_access_token({"sub": user.email}),
            token_type="Bearer"
        )
    )
