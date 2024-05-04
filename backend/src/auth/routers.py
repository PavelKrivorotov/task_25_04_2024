from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.responses import Response, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session

from auth.depends import is_authenticated
from auth.schemas import CreateUser
from auth.crud import auth_crud
from auth.models import User

from job.validations import validate_job_exists


router = APIRouter()


@router.post('/register')
async def register(
    data: Annotated[CreateUser, Depends()],
    db: AsyncSession = Depends(get_async_session)
):

    user = await auth_crud.get_user_by_username(db, data.username)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with username `{}` already exists'.format(data.username)
        )
    
    job_exists = await validate_job_exists(db, data.job_id)
    if not job_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Job `{}` is not exists'.format(data.job_id)
        )
    
    user = await auth_crud.create(db, data)
    return JSONResponse(
        content=user,
        status_code=status.HTTP_201_CREATED
    )


@router.post('/login')
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session)
):
    
    data = await auth_crud.login(db, form.username, form.password)
    return data


@router.post('/logout')
async def logout(
    user: User = Depends(is_authenticated),
    db: AsyncSession = Depends(get_async_session)
):
    await auth_crud.logout(db, user.id)
    return Response(status_code=status.HTTP_200_OK)

