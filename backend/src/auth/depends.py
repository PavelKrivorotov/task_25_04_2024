import datetime
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app import settings
from app.db import get_async_session

from auth.models import User
from auth.mixins import MixinTokenCRUD, MixinUserCRUD


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login', auto_error=False)


async def is_authenticated(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_async_session)]
) -> User:
    
    instance = await MixinTokenCRUD.get_token_by_key(db, token)
    if instance is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    delta = datetime.timedelta(seconds=settings.TOKEN_EXPIRE_TIME)
    if (datetime.datetime.now() - instance.created) > delta:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await MixinUserCRUD.get_user_by_token(db, token)
    return user


async def is_staff(
    user: Annotated[User, Depends(is_authenticated)]
) -> User:
    
    if user.is_staff:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid permissions. Allowed only `Staff`'
    )


async def is_admin(
    user: Annotated[User, Depends(is_authenticated)]
) -> User:
    
    if user.is_superuser:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Invalid permissions. Allowed only `Admin`'
    )

