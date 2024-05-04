import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, Token
from auth.mixins import MixinUserCRUD, MixinTokenCRUD
from auth.utils import hash_password


mixin_user_crud = MixinUserCRUD()
mixin_token_crud = MixinTokenCRUD()


class TestMixinUserCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_get_user_by_username(self,  db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('f170c946-8619-424f-b2ee-e946195796c6'),
            'username': 'get-user-by-username-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('90a7e79d-df6c-4e1b-8bc7-608b83afbc41'),
            'username': 'get-user-by-username-user1',
            'password': 'w3d',
            'first_name': 'TestMixinUserUser1',
            'last_name': 'TestMixinUserUser1',
            'is_staff': True,
            'is_superuser': False
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        u2 = user_2.copy()
        u2['password'] = hash_password(u2['password'])
        user1 = User(**u2)

        user1 = User(**u1)
        user2 = User(**u2)

        db_session.add_all([user1, user2])
        await db_session.commit()
        
        exists_user1 = await mixin_user_crud.get_user_by_username(db_session, user_1['username'])
        assert isinstance(exists_user1, User)

        exists_user2 = await mixin_user_crud.get_user_by_username(db_session, user_2['username'])
        assert isinstance(exists_user2, User)


        # clear db
        await db_session.delete(user1)
        await db_session.delete(user2)
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_get_user_by_token(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('bcffdeba-a9ce-4387-b2da-b89733057552'),
            'username': 'get_user_by_token-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('7f1f6890-b4f5-4d25-af3d-02153222af53'),
            'username': 'get_user_by_token-user1',
            'password': 'w3d',
            'first_name': 'TestMixinUserUser1',
            'last_name': 'TestMixinUserUser1',
            'is_staff': True,
            'is_superuser': False
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        u2 = user_2.copy()
        u2['password'] = hash_password(u2['password'])
        user1 = User(**u2)

        user1 = User(**u1)
        user2 = User(**u2)

        db_session.add_all([user1, user2])
        await db_session.commit()

        token_1 = {
            'key': '1695da8074d0a8aa8adb165b22cc8668d24a1b8d7cfbda36',
            'user_id': uuid.UUID('bcffdeba-a9ce-4387-b2da-b89733057552')
        }
        token_2 = {
            'key': '21efac13f4d4ec3381c0a9b02cd5b60db2fedb20b1e83b2c',
            'user_id': uuid.UUID('7f1f6890-b4f5-4d25-af3d-02153222af53')
        }

        token1 = Token(**token_1)
        token2 = Token(**token_2)

        db_session.add_all([token1, token2])
        await db_session.commit()

        exists_user1 = await MixinUserCRUD.get_user_by_token(db_session, token_1['key'])
        assert isinstance(exists_user1, User)

        exists_user2 = await MixinUserCRUD.get_user_by_token(db_session, token_2['key'])
        assert isinstance(exists_user2, User)


        # clear db
        await db_session.delete(user1)
        await db_session.delete(user2)
        await db_session.delete(token1)
        await db_session.delete(token2)
        await db_session.commit()

    
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_get_verify_user(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('d193fa9c-86fd-42b1-89db-354f09eb34d0'),
            'username': 'get_verify_user-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        db_session.add(user1)
        await db_session.commit()

        exists_user_1 = await mixin_user_crud.get_verify_user(
            db=db_session,
            username=user_1['username'],
            password=user_1['password']
        )
        assert isinstance(exists_user_1, User)

        exists_user_2 = await mixin_user_crud.get_verify_user(
            db=db_session,
            username=user_1['username'],
            password='fake-password'
        )
        assert exists_user_2 is None

        exists_user_3 = await mixin_user_crud.get_verify_user(
            db=db_session,
            username='fake-username',
            password='fake-password'
        )
        assert exists_user_3 is None


        # clear db
        await db_session.delete(user1)
        await db_session.commit()


class TestMixinTokenCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_get_token_by_key(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('cc9d2dd9-03c9-42f2-a351-c053d19393c7'),
            'username': 'get_token_by_key-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        user1 = User(**u1)

        db_session.add(user1)
        await db_session.commit()

        token_1 = {
            'key': '060b54d783b8cfcc7adac72c29a7f032c188312e180a80c7',
            'user_id': uuid.UUID('cc9d2dd9-03c9-42f2-a351-c053d19393c7')
        }

        token1 = Token(**token_1)

        db_session.add(token1)
        await db_session.commit()

        exists_token1 = await MixinTokenCRUD.get_token_by_key(db_session, token_1['key'])
        assert isinstance(exists_token1, Token)

        exists_token2 = await MixinTokenCRUD.get_token_by_key(db_session, 'fake-access-token-key')
        assert exists_token2 is None


        # clear db
        await db_session.delete(user1)
        await db_session.delete(token1)
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_get_token_by_user_id(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('2608bd46-bc69-4e85-b864-95193977b793'),
            'username': 'get_token_by_user_id-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        user1 = User(**u1)

        db_session.add(user1)
        await db_session.commit()

        token_1 = {
            'key': 'a1b66fe28591e81b4de6cf26f1ae821f680014e2b14a95bd',
            'user_id': uuid.UUID('2608bd46-bc69-4e85-b864-95193977b793')
        }

        token1 = Token(**token_1)

        db_session.add(token1)
        await db_session.commit()

        exists_token1 = await mixin_token_crud.get_token_by_user_id(db_session, user_1['id'])
        assert isinstance(exists_token1, Token)

        # fale user uuid
        exists_token2 = await mixin_token_crud.get_token_by_user_id(
            db=db_session,
            user_id=uuid.UUID('11111111-1111-1111-1111-111111111111')
        )
        assert exists_token2 is None


        # clear db
        await db_session.delete(user1)
        await db_session.delete(token1)
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_create_token(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('f9858d58-a753-45cd-acff-7cb31795f6b1'),
            'username': 'create_token-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        user1 = User(**u1)

        db_session.add(user1)
        await db_session.commit()

        token1 = await mixin_token_crud.create_token(db_session, user_1['id'])
        assert isinstance(token1, Token)
        assert token1.user_id == user_1['id']


        # clear db
        await db_session.delete(user1)
        await db_session.delete(token1)
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_refresh_token(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('758fcc15-460e-4f8f-a67b-ea7f5c84856c'),
            'username': 'refresh_token-admin1',
            'password': 'admin',
            'first_name': 'TestMixinUserCRUDAdmin1',
            'last_name': 'TestMixinUserCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        user1 = User(**u1)

        db_session.add(user1)
        await db_session.commit()

        token_1 = {
            'key': 'e3b57df638638155616e1e5a0a0fa25ff56d42f0a701f7b8',
            'user_id': uuid.UUID('758fcc15-460e-4f8f-a67b-ea7f5c84856c')
        }

        token1 = Token(**token_1)

        db_session.add(token1)
        await db_session.commit()

        new_token1 = await mixin_token_crud.refresh_token(db_session, user_1['id'], token1)
        assert new_token1.key != token_1['key']
        assert new_token1.user_id == user_1['id']

        old_token1 = await db_session.get(Token, token_1['key'])
        assert old_token1 is None


        # clear db
        await db_session.delete(user1)
        await db_session.delete(new_token1)
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_create_or_refresh_token(self, db_session: AsyncSession):
        user_1 = {
            'id': uuid.UUID('ffd0e08c-cf43-4f87-98ce-a2542b998fd8'),
            'username': 'create_or_refresh_token-user1',
            'password': 'wdef',
            'first_name': 'TestMixinUserCRUDUser1',
            'last_name': 'TestMixinUserCRUDUser1',
            'is_staff': True,
            'is_superuser': False
        }
        user_2 = {
            'id': uuid.UUID('a56806b1-a78c-4224-8d4e-0c4a2531fe9e'),
            'username': 'create_or_refresh_token-user2',
            'password': '7e2u',
            'first_name': 'TestMixinUserCRUDUser2',
            'last_name': 'TestMixinUserCRUDUser2',
            'is_staff': True,
            'is_superuser': False
        }

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        u2 = user_2.copy()
        u2['password'] = hash_password(u2['password'])
        user2 = User(**u2)

        db_session.add_all([user1, user2])
        await db_session.commit()

        token_1 = {
            'key': 'f41c621e5d487c5ca580b17fc04771e31e0fbd71667aa168',
            'user_id': uuid.UUID('ffd0e08c-cf43-4f87-98ce-a2542b998fd8')
        }

        token1 = Token(**token_1)

        db_session.add(token1)
        await db_session.commit()

        new_token1 = await mixin_token_crud.create_or_refresh_token(db_session, user_1['id'])
        assert new_token1.key != token_1['key']
        assert new_token1.user_id == user_1['id']

        old_token1 = await db_session.get(Token, token_1['key'])
        assert old_token1 is None

        token2 = await mixin_token_crud.create_or_refresh_token(db_session, user_2['id'])
        assert token2.user_id == user_2['id']


        # clear db
        await db_session.delete(user1)
        await db_session.delete(user2)
        await db_session.delete(new_token1)
        await db_session.delete(token2)
        await db_session.commit()

