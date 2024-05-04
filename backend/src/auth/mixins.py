import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, Token
from auth.utils import (
    check_password,
    generate_authorization_token
)


class MixinUserCRUD:
    @classmethod
    async def get_user_by_username(
        cls,
        db: AsyncSession,
        username: str
    ) -> Optional[User]:
        
        query = select(User).where(User.username == username)
        user = await db.scalar(query)
        return user

    @classmethod
    async def get_user_by_token(
        cls,
        db: AsyncSession,
        token: str
    ) -> Optional[User]:
        
        query = (
            select(User)
            .join_from(User, Token, User.id == Token.user_id)
            .where(Token.key == token)
        )
        user = await db.scalar(query)
        return user
    
    async def get_verify_user(
        self,
        db: AsyncSession,
        username: str,
        password: str
    ) -> Optional[User]:

        user = await self.get_user_by_username(db, username)
        if user is None:
            return None
        
        if not check_password(password, user.password):
            return None
        
        return user
    

class MixinTokenCRUD:
    @classmethod
    async def get_token_by_key(
        cls,
        db: AsyncSession,
        key: str
    ) -> Optional[Token]:
        
        query = select(Token).where(Token.key == key)
        token = await db.scalar(query)
        return token

    async def get_token_by_user_id(
        self,
        db: AsyncSession,
        user_id: uuid.UUID
    ) -> Optional[Token]:
        
        query = select(Token).where(Token.user_id == user_id)
        token = await db.scalar(query)
        return token

    async def create_token(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
    ) -> Token:
        
        token = Token(
            key=generate_authorization_token(),
            user_id=user_id
        )

        db.add(token)
        await db.commit()
        await db.refresh(token)

        return token

    async def refresh_token(
        self,
        db: AsyncSession,
        user_id: uuid.UUID,
        token: Token
    ) -> Token:
        
        await db.delete(token)
        await db.commit()
        
        token = await self.create_token(db, user_id)
        return token

    async def create_or_refresh_token(
        self,
        db: AsyncSession,
        user_id: uuid.UUID
    ) -> Token:
        
        token = await self.get_token_by_user_id(db, user_id)
        if token is None:
            token = await self.create_token(db, user_id)
            return token
        
        token = await self.refresh_token(db, user_id, token)
        return token
    
