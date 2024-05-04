import uuid
import datetime
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_external_url_to_route
from auth import urls as auth_urls
from auth.models import User, Token
from auth.utils import hash_password, check_password

from employee import urls as employee_urls

from job import urls as job_urls
from job.models import Job, UserJob

from tests.utils import add_authorization_header


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_register(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('648e7c0c-1ced-4bd3-8a29-40c0ed19569a'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('6b94aa2b-1be5-4530-8145-1340cfb4497d'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }
    job_3 = {
        'id': uuid.UUID('91e39c7a-0e71-4472-8c9c-9be760937a14'),
        'title': 'Middle python developer',
        'salary': 120000,
        'days_to_promotion': datetime.timedelta(days=540)
    }
    job_4 = {
        'id': uuid.UUID('bc4a3232-88ce-4251-be32-dcb5234e2e1a'),
        'title': 'Senior python developer',
        'salary': 220000,
        'days_to_promotion': datetime.timedelta(days=790)
    }

    job1 = Job(**job_1)
    job2 = Job(**job_2)
    job3 = Job(**job_3)
    job4 = Job(**job_4)

    db_session.add_all([job1, job2, job3, job4])
    await db_session.commit()

    user_1 = {
        'username': 'user1',
        'password': 'ojwdu83yt7eg',
        'first_name': 'User1',
        'last_name': 'UUser1',
        'job_id': '648e7c0c-1ced-4bd3-8a29-40c0ed19569a'
    }
    user_2 = {
        'username': None,
        'password': 'jjjh321s1111',
        'first_name': 'User2',
        'last_name': 'UUser2',
        'job_id': '6b94aa2b-1be5-4530-8145-1340cfb4497d'
    }
    user_3 = {
        'username': 'my-user3',
        'password': None,
        'first_name': 'User3',
        'last_name': 'UUser3',
        'job_id': '91e39c7a-0e71-4472-8c9c-9be760937a14'
    }
    user_4 = {
        'username': 'my-user4',
        'password': 'hello',
        'first_name': None,
        'last_name': 'UUser4',
        'job_id': 'bc4a3232-88ce-4251-be32-dcb5234e2e1a'
    }
    user_5 = {
        'username': 'my-user5',
        'password': 'k1',
        'first_name': 'User5',
        'last_name': None,
        'job_id': 'bc4a3232-88ce-4251-be32-dcb5234e2e1a'
    }
    user_6 = {
        'username': 'user6',
        'password': 'he87-12ksf',
        'first_name': 'User6',
        'last_name': 'UUser6',
        'job_id': 'any-content-this'
    }
    user_7 = {
        'username': 'user7',
        'password': 'slojs92',
        'first_name': 'User7',
        'last_name': 'UUser7',
        'job_id': '11111111-1111-1111-1111-111111111111'
    }

    response_1 = await async_client.post(url=auth_urls.Register_Url, data=user_1, headers=headers)
    assert response_1.status_code == 201
    assert response_1.json() == {
        'user': get_external_url_to_route(employee_urls.Me_Url),
        'job': get_external_url_to_route(job_urls.Me_Url)
    }

    query = select(User).where(User.username == user_1['username'])
    user = await db_session.scalar(query)

    assert isinstance(user, User)
    assert user.password != user_1['password']
    assert check_password(user_1['password'], user.password)
    assert user.first_name == user_1['first_name']
    assert user.last_name == user_1['last_name']
    assert user.is_staff == True
    assert user.is_superuser == False

    query = select(UserJob).where(UserJob.user_id == user.id)
    user_job = await db_session.scalar(query)

    assert isinstance(user_job, UserJob)
    assert str(user_job.job_id) == user_1['job_id']

    await db_session.delete(user)
    await db_session.commit()

    response_2 = await async_client.post(url=auth_urls.Register_Url, data=user_2, headers=headers)
    assert response_2.status_code == 422

    response_3 = await async_client.post(url=auth_urls.Register_Url, data=user_3,headers=headers)
    assert response_3.status_code == 422

    response_4 = await async_client.post(url=auth_urls.Register_Url, data=user_4, headers=headers)
    assert response_4.status_code == 422

    response_5 = await async_client.post(url=auth_urls.Register_Url, data=user_5, headers=headers)
    assert response_5.status_code == 422

    response_6 = await async_client.post(url=auth_urls.Register_Url, data=user_6, headers=headers)
    assert response_6.status_code == 422

    response_7 = await async_client.post(url=auth_urls.Register_Url, data=user_7, headers=headers)
    assert response_7.status_code == 400
    assert response_7.json() == {
        'detail': 'Job `{0}` is not exists'.format(
            user_7['job_id']
        )
    }


    # clear db
    await db_session.execute(delete(Job))
    await db_session.commit()


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_login(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('0dc7b7c1-96be-4c00-846f-4372a97265f7'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('0984aad0-8cac-4e70-bab9-fb24634e2103'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }

    user_1 = {
        'id': uuid.UUID('6f9c746a-1159-4661-8ced-83ccdf896620'),
        'username': 'login-admin1',
        'password': 'admin',
        'first_name': 'LoginAdmin1',
        'last_name': 'LoginAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('50bb5af1-1076-4523-8fd0-1c72aca8caa8'),
        'username': 'login-user-1',
        'password': 'jjjh321s1111',
        'first_name': 'LoginUser1',
        'last_name': 'LoginUser2',
        'is_staff': True,
        'is_superuser': False
    }
    user_3 = {
        'id': uuid.UUID('a8c5b2e5-cbfc-407e-85fb-a96c864f3554'),
        'username': 'login-user-2',
        'password': '9982vy9e',
        'first_name': 'LoginUser2',
        'last_name': 'LoginUser3',
        'is_staff': True,
        'is_superuser': False
    }

    job1 = Job(**job_1)
    job2 = Job(**job_2)

    u1 = user_1.copy()
    u1['password'] = hash_password(u1['password'])
    user1 = User(**u1)

    u2 = user_2.copy()
    u2['password'] = hash_password(u2['password'])
    user2 = User(**u2)

    u3 = user_3.copy()
    u3['password'] = hash_password(u3['password'])
    user3 = User(**u3)

    db_session.add_all([job1, job2, user1, user2, user3])
    await db_session.commit()

    user_job_1 = {
        'id': uuid.UUID('989b35ee-4b75-459e-91c6-5ced56da96d5'),
        'job_id': uuid.UUID('0dc7b7c1-96be-4c00-846f-4372a97265f7'),
        'user_id': uuid.UUID('50bb5af1-1076-4523-8fd0-1c72aca8caa8')
    }
    user_job_2 = {
        'id': uuid.UUID('bbd3ff60-8f80-4000-9d05-49b754ecab8a'),
        'job_id': uuid.UUID('0984aad0-8cac-4e70-bab9-fb24634e2103'),
        'user_id': uuid.UUID('a8c5b2e5-cbfc-407e-85fb-a96c864f3554')
    }

    user_job1 = UserJob(**user_job_1)
    user_job2 = UserJob(**user_job_2)

    db_session.add_all([user_job1, user_job2])
    await db_session.commit()

    login_1 = {
        'username': 'login-admin1',
        'password': 'admin'
    }
    login_2 = {
        'username': 'login-user-1',
        'password': 'jjjh321s1111'
    }
    login_3 = {
        'username': 'login-user-2',
        'password': '9982vy9e'
    }
    login_4 = {
        'username': 'fake-admin-login',
        'password': 'admin'
    }
    login_5 = {
        'username': 'login-admin',
        'password': 'fake-admin-password'
    }
    login_6 = {
        'username': None,
        'password': None
    }

    response_1 = await async_client.post(url=auth_urls.Login_Url, data=login_1, headers=headers)
    query = select(Token).where(Token.user_id == user_1['id'])
    token1 = await db_session.scalar(query)

    assert response_1.status_code == 200
    assert isinstance(token1, Token)
    assert response_1.json() == {
        'access_token': token1.key,
        'token_type': 'bearer',
        'is_superuser': True
    }

    response_2 = await async_client.post(url=auth_urls.Login_Url, data=login_2, headers=headers)
    query = select(Token).where(Token.user_id == user_2['id'])
    token2 = await db_session.scalar(query)

    assert response_2.status_code == 200
    assert isinstance(token2, Token)
    assert response_2.json() == {
        'access_token': token2.key,
        'token_type': 'bearer',
        'is_superuser': False
    }

    response_3 = await async_client.post(url=auth_urls.Login_Url, data=login_3, headers=headers)
    query = select(Token).where(Token.user_id == user_3['id'])
    token3 = await db_session.scalar(query)

    assert response_3.status_code == 200
    assert isinstance(token3, Token)
    assert response_3.json() == {
        'access_token': token3.key,
        'token_type': 'bearer',
        'is_superuser': False
    }

    response_4 = await async_client.post(url=auth_urls.Login_Url, data=login_4, headers=headers)
    assert response_4.status_code == 400
    assert response_4.json() == {
        'detail': 'The credential will not provided'
    }

    response_5 = await async_client.post(url=auth_urls.Login_Url, data=login_5, headers=headers)
    assert response_5.status_code == 400
    assert response_5.json() == {
        'detail': 'The credential will not provided'
    }

    response_6 = await async_client.post(url=auth_urls.Login_Url, data=login_6, headers=headers)
    assert response_6.status_code == 422

    await db_session.delete(token1)
    await db_session.delete(token2)
    await db_session.delete(token2)
    await db_session.commit()


    # clear db
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(User))
    await db_session.execute(delete(Job))
    await db_session.commit()


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_logout(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('445c2973-6951-42f2-bb66-3813edadfb94'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    user_1 = {
        'id': uuid.UUID('312474a0-5ab2-446c-b8d6-eceb42fd8ddf'),
        'username': 'logout-admin1',
        'password': 'admin',
        'first_name': 'LogoutAdmin1',
        'last_name': 'LogoutAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('0ed889b2-9663-4f9a-a398-7dabbbeafb96'),
        'username': 'logout-user-1',
        'password': 'sw34',
        'first_name': 'LogoutUser1',
        'last_name': 'LogoutUser2',
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
        'id': uuid.UUID('e298ffa2-e9fc-4510-a0e4-7b80b5e29e2f'),
        'job_id': uuid.UUID('445c2973-6951-42f2-bb66-3813edadfb94'),
        'user_id': uuid.UUID('0ed889b2-9663-4f9a-a398-7dabbbeafb96')
    }

    token_1 = {
        'key': 'a6978592e6faa853ef9c4399c1add477011baa3103069927',
        'user_id': uuid.UUID('312474a0-5ab2-446c-b8d6-eceb42fd8ddf')
    }
    token_2 = {
        'key': 'dd1bccfe82149503173825884415f1a1ce5dadac35781764',
        'user_id': uuid.UUID('0ed889b2-9663-4f9a-a398-7dabbbeafb96')
    }

    user_job2 = UserJob(**user_job_2)
    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.post(url=auth_urls.Logout_Url, headers=headers1)
    assert response_1.status_code == 200

    token_db1 = await db_session.get(Token, token1.key)
    assert token_db1 is None

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.post(url=auth_urls.Logout_Url, headers=headers2)
    assert response_2.status_code == 200

    token_db2 = await db_session.get(Token, token2.key)
    assert token_db2 is None

    headers3 = add_authorization_header('fake-access-token-key', headers)
    response_3 = await async_client.post(url=auth_urls.Logout_Url, headers=headers3)
    assert response_3.status_code == 401
    assert response_3.json() == {'detail': 'Unauthorized'}

    response_4 = await async_client.post(url=auth_urls.Logout_Url, headers=headers)
    assert response_4.status_code == 401
    assert response_4.json() == {'detail': 'Unauthorized'}


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()

