import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, Token
from auth.schemas import CreateUser, RepresentUser
from auth.mixins import MixinUserCRUD, MixinTokenCRUD
from auth.utils import hash_password

from job.models import UserJob


class AuthCRUD(MixinUserCRUD, MixinTokenCRUD):
    async def create(
        self,
        db: AsyncSession,
        data: CreateUser
    ) -> dict[str, Any]:
        
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            username=data.username,
            password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name
        )

        user_job = UserJob(
            user_id=user_id,
            job_id=data.job_id
        )

        db.add_all([user, user_job])
        await db.commit()

        return RepresentUser().model_dump()

    async def login(
        self,
        db: AsyncSession,
        username: str,
        password: str
    ) -> dict[str, Any]:
        
        user = await self.get_verify_user(db, username, password)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='The credential will not provided'
            )
        
        token = await self.create_or_refresh_token(db, user.id)
        return {
            'access_token': token.key,
            'token_type': 'bearer',
            'is_superuser': user.is_superuser
        }

    async def logout(
        self,
        db: AsyncSession,
        user_id: uuid.UUID
    ) -> None:
        
        query = delete(Token).where(Token.user_id == user_id)
        await db.execute(query)
        await db.commit()

auth_crud = AuthCRUD()

