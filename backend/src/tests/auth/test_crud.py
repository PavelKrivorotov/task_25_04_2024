import uuid
import datetime

import pytest
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_external_url_to_route
from auth.models import User, Token
from auth.schemas import CreateUser
from auth.crud import auth_crud
from auth.utils import hash_password, check_password

from employee import urls as employee_urls

from job import urls as job_urls
from job.models import Job, UserJob


class TestAuthCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_register(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('0755e1df-461b-47d3-ad3a-98dfc78931cb'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        job1 = Job(**job_1)
        db_session.add(job1)
        await db_session.commit()

        user_1 = {
            'username': 'register-crud-user1',
            'password': 'ko8ye72ge',
            'first_name': 'RegisterCRUDUser1',
            'last_name': 'RegisterCRUDUser1',
            'job_id': '0755e1df-461b-47d3-ad3a-98dfc78931cb'
        }

        data_user_1 = CreateUser(**user_1)
        result_1 = await auth_crud.create(db_session, data_user_1)
        assert result_1 == {
            'user': get_external_url_to_route(employee_urls.Me_Url),
            'job': get_external_url_to_route(job_urls.Me_Url)
        }

        query1 = select(User).where(User.username == user_1['username'])
        user1 = await db_session.scalar(query1)
        assert isinstance(user1, User)
        assert user1.password != user_1['password']
        assert check_password(user_1['password'], user1.password) == True
        assert user1.username == user_1['username']
        assert user1.first_name == user_1['first_name']
        assert user1.last_name == user_1['last_name']
        assert user1.is_staff == True
        assert user1.is_superuser == False

        query2 = select(UserJob).where(UserJob.user_id == user1.id)
        user_job1 = await db_session.scalar(query2)
        assert user_job1.job_id == job_1['id']


        # clear db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_login(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('29a24d23-14ce-43d0-89fb-a46ae6776ef2'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        user_1 = {
            'id': uuid.UUID('dd100c48-4484-435e-995f-8b4c06dace12'),
            'username': 'login-crud-admin1',
            'password': 'admin',
            'first_name': 'LoginCRUDAdmin1',
            'last_name': 'LoginCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('a8ff79d2-03af-4154-a088-63e1524979d0'),
            'username': 'login-crud-user1',
            'password': 'ko8ye72ge',
            'first_name': 'LoginCRUDUser1',
            'last_name': 'LoginCRUDUser1',
            'is_staff': True,
            'is_superuser': False
        }

        job1 = Job(**job_1)

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        u2 = user_2.copy()
        u2['password'] = hash_password(u2['password'])
        user2 = User(**u2)

        db_session.add_all([job1, user1, user2])
        await db_session.commit()

        user_job_2 = {
            'id': uuid.UUID('6eced603-3ccd-485b-81dc-a8fccc35a9d9'),
            'job_id': uuid.UUID('29a24d23-14ce-43d0-89fb-a46ae6776ef2'),
            'user_id': uuid.UUID('a8ff79d2-03af-4154-a088-63e1524979d0')
        }

        user_job2 = UserJob(**user_job_2)
        db_session.add(user_job2)
        await db_session.commit()

        response_1 = await auth_crud.login(db_session, user_1['username'], user_1['password'])
        query1 = select(Token).where(Token.user_id == user_1['id'])
        token1 = await db_session.scalar(query1)
        assert response_1 == {
            'access_token': token1.key,
            'token_type': 'bearer',
            'is_superuser': True
        }

        response_2 = await auth_crud.login(db_session, user_2['username'], user_2['password'])
        query2 = select(Token).where(Token.user_id == user_2['id'])
        token2 = await db_session.scalar(query2)
        assert response_2 == {
            'access_token': token2.key,
            'token_type': 'bearer',
            'is_superuser': False
        }


        # cleae db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.execute(delete(Token))
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_logout(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('9f7d0cb2-07f7-40a9-a400-4819801a5558'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        user_1 = {
            'id': uuid.UUID('b5ee17a0-7bac-4cb0-bb70-cf1204295599'),
            'username': 'logout-crud-admin1',
            'password': 'admin',
            'first_name': 'LogoutCRUDAdmin1',
            'last_name': 'LogoutCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('769da8fe-e78a-479d-87c6-12c8c7d25ea1'),
            'username': 'logout-crud-user1',
            'password': '7t2ygs',
            'first_name': 'LogoutCRUDUser1',
            'last_name': 'LogoutCRUDUser1',
            'is_staff': True,
            'is_superuser': False
        }

        job1 = Job(**job_1)

        u1 = user_1.copy()
        u1['password'] = hash_password(u1['password'])
        user1 = User(**u1)

        u2 = user_2.copy()
        u2['password'] = hash_password(u2['password'])
        user2 = User(**u2)

        db_session.add_all([job1, user1, user2])
        await db_session.commit()

        user_job_2 = {
            'id': uuid.UUID('7fddcc79-a235-4581-b676-6ecea06a5ba6'),
            'job_id': uuid.UUID('9f7d0cb2-07f7-40a9-a400-4819801a5558'),
            'user_id': uuid.UUID('769da8fe-e78a-479d-87c6-12c8c7d25ea1')
        }

        token_1 = {
            'key': '84afe20963aa15dde77079435747d0ec2a3f4b69c8791679',
            'user_id': uuid.UUID('b5ee17a0-7bac-4cb0-bb70-cf1204295599')
        }
        token_2 = {
            'key': 'ae7eebffbbcd049643c206e31f7bf7c0f8df317023d25503',
            'user_id': uuid.UUID('769da8fe-e78a-479d-87c6-12c8c7d25ea1')
        }

        user_job2 = UserJob(**user_job_2)

        token1 = Token(**token_1)
        token2 = Token(**token_2)

        db_session.add_all([user_job2, token1, token2])
        await db_session.commit()

        response_1 = await auth_crud.logout(db_session, user_1['id'])
        assert response_1 is None

        exists_token1 = await db_session.get(Token, token_1['key'])
        assert exists_token1 is None

        response_2 = await auth_crud.logout(db_session, user_2['id'])
        assert response_2 is None

        exists_token2 = await db_session.get(Token, token_2['key'])
        assert exists_token2 is None


        # clear db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.execute(delete(Token))
        await db_session.commit()

