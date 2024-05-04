import re
import uuid
import datetime
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_external_url_to_route
from auth.models import User, Token
from auth.utils import hash_password
from job.models import Job, UserJob
from admin.job import urls as admin_job_urls

from tests.utils import add_authorization_header


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_create_job(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any]
):
    user_1 = {
        'id': uuid.UUID('d06dfb1c-f136-45fa-93fb-c168c9114954'),
        'username': 'admin-create-job-admin1',
        'password': 'admin',
        'first_name': 'AdminCreateJobAdmin1',
        'last_name': 'AdminCreateJobAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('9842a36a-d5c9-4a96-b5ba-fa539a14120d'),
        'username': 'admin-creat-job-user-1',
        'password': '9hdca',
        'first_name': 'AdmiCreateJobsUser1',
        'last_name': 'AdminCeateJobsUser2',
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
        'key': 'c7f9e93160c712d6270f8b74c757557f45590c50632fdeaf',
        'user_id': uuid.UUID('d06dfb1c-f136-45fa-93fb-c168c9114954')
    }
    token_2 = {
        'key': '450c15ed7bebfb39b8adaec80ffa216063b091ae14849bed',
        'user_id': uuid.UUID('9842a36a-d5c9-4a96-b5ba-fa539a14120d')
    }

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([token1, token2])
    await db_session.commit()

    job_1 = {
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': 180
    }
    job_2 = {
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': 365
    }

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.post(url=admin_job_urls.Job_Create_Url, data=job_1, headers=headers1)
    url_to_job = response_1.json().get('job', None)
    assert response_1.status_code == 201
    assert isinstance(url_to_job, str)
    assert len(list(response_1.json())) == 1

    url = get_external_url_to_route(admin_job_urls.Job_Single_Url.format(''))

    pattern_uuid = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
    pattern_url = '^{0}{1}$'.format(url, pattern_uuid)

    match_url_to_job = re.fullmatch(pattern_url, url_to_job)
    assert isinstance(match_url_to_job, re.Match)
    assert match_url_to_job[0] == url_to_job

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.post(url=admin_job_urls.Job_Create_Url, data=job_2, headers=headers2)
    assert response_2.status_code == 403
    assert response_2.json() == {'detail': 'Invalid permissions. Allowed only `Admin`'}


    # cleaer database
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(Token))
    await db_session.commit()


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_list_jobs(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('513f70bf-0d6f-43ea-92c5-1c7f52fbf231'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('5460b684-4184-47fa-9afa-8e397c9c7284'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }
    job_3 = {
        'id': uuid.UUID('fce87175-e181-49cf-a7e7-9f7559cef822'),
        'title': 'Middle python developer',
        'salary': 120000,
        'days_to_promotion': datetime.timedelta(days=540)
    }

    user_1 = {
        'id': uuid.UUID('b4d346f1-e5ec-4cdd-b528-84e004119f8b'),
        'username': 'admin-list-jobs-admin1',
        'password': 'admin',
        'first_name': 'AdminListJobsAdmin1',
        'last_name': 'AdminListJobsAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('f5a7f396-4959-4a08-80b2-42a17b123711'),
        'username': 'admin-list-jobs-user-1',
        'password': '9hdca',
        'first_name': 'AdminListJobsUser1',
        'last_name': 'AdminListJobsUser2',
        'is_staff': True,
        'is_superuser': False
    }

    job1 = Job(**job_1)
    job2 = Job(**job_2)
    job3 = Job(**job_3)

    u1 = user_1.copy()
    u1['password'] = hash_password(u1['password'])
    user1 = User(**u1)

    u2 = user_2.copy()
    u2['password'] = hash_password(u2['password'])
    user2 = User(**u2)

    db_session.add_all([job1, job2, job3, user1, user2])
    await db_session.commit()

    user_job_2 = {
        'id': uuid.UUID('e3354b2b-dd69-4cef-b07b-b984f69c3064'),
        'job_id': uuid.UUID('513f70bf-0d6f-43ea-92c5-1c7f52fbf231'),
        'user_id': uuid.UUID('f5a7f396-4959-4a08-80b2-42a17b123711')
    }

    token_1 = {
        'key': '65c1ae5bd9986299fafb1dbc9e8a095a25f93ed32d8b81d9',
        'user_id': uuid.UUID('b4d346f1-e5ec-4cdd-b528-84e004119f8b')
    }
    token_2 = {
        'key': '0a2ff5577c95ea52819a52c452d4718b6556c8ffd9feda99',
        'user_id': uuid.UUID('f5a7f396-4959-4a08-80b2-42a17b123711')
    }

    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    json_result = {
        'count': 3,
        'results': [
            {
                'id': '513f70bf-0d6f-43ea-92c5-1c7f52fbf231',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            },
            {
                'id': '5460b684-4184-47fa-9afa-8e397c9c7284',
                'title': 'Junior python developer',
                'salary': 50000,
                'days_to_promotion': 365
            }, 
            {
                'id': 'fce87175-e181-49cf-a7e7-9f7559cef822',
                'title': 'Middle python developer',
                'salary': 120000,
                'days_to_promotion': 540
            }
        ]
    }

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.get(url=admin_job_urls.Job_All_Url, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_result

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.get(url=admin_job_urls.Job_All_Url, headers=headers2)
    assert response_2.status_code == 403
    assert response_2.json() == {'detail': 'Invalid permissions. Allowed only `Admin`'}

    headers3 = add_authorization_header('fake-access-token-key', headers)
    response_3 = await async_client.get(url=admin_job_urls.Job_All_Url, headers=headers3)
    assert response_3.status_code == 401
    assert response_3.json() == {'detail': 'Unauthorized'}

    response_4 = await async_client.get(url=admin_job_urls.Job_All_Url, headers=headers)
    assert response_4.status_code == 401
    assert response_4.json() == {'detail': 'Unauthorized'}


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_retrieve_job(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('e689b116-8b75-4801-8ba9-86165cba9e4e'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    user_1 = {
        'id': uuid.UUID('f3ecca90-e57a-4763-9ee8-bd7a701838e0'),
        'username': 'admin-single-jobs-admin1',
        'password': 'admin',
        'first_name': 'Admin-SingleJobsAdmin1',
        'last_name': 'Admin-SingleJobsAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('82a5bba0-84a8-425e-b4f8-ab44d5103a9a'),
        'username': 'admin-single-jobs-user-1',
        'password': '9v62ghs',
        'first_name': 'AdminSingleJobsUser1',
        'last_name': 'AdminSingleJobsUser2',
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
        'id': uuid.UUID('e17b590b-2b95-4cf1-b1f7-f9db894ddecc'),
        'job_id': uuid.UUID('e689b116-8b75-4801-8ba9-86165cba9e4e'),
        'user_id': uuid.UUID('82a5bba0-84a8-425e-b4f8-ab44d5103a9a')
    }

    token_1 = {
        'key': '0e63940e434a041bb0870aba3ed7def52d2aad1111158db0',
        'user_id': uuid.UUID('f3ecca90-e57a-4763-9ee8-bd7a701838e0')
    }
    token_2 = {
        'key': '43514e1adae2bbc42b57a54888efba24513995a6278b5547',
        'user_id': uuid.UUID('82a5bba0-84a8-425e-b4f8-ab44d5103a9a')
    }

    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    json_job = {
        'job': {
            'id': 'e689b116-8b75-4801-8ba9-86165cba9e4e',
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': 180
        }
    }

    headers1 = add_authorization_header(token1.key, headers)
    url1 = admin_job_urls.Job_Single_Url.format(job_1['id'])
    response_1 = await async_client.get(url=url1, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_job

    headers2 = add_authorization_header(token2.key, headers)
    url2 = admin_job_urls.Job_Single_Url.format(job_1['id'])
    response_2 = await async_client.get(url=url2, headers=headers2)
    assert response_2.status_code == 403
    assert response_2.json() == {'detail': 'Invalid permissions. Allowed only `Admin`'}

    headers3 = add_authorization_header('fake-access-token-key', headers)
    url3 = admin_job_urls.Job_Single_Url.format(job_1['id'])
    response_3 = await async_client.get(url=url3, headers=headers3)
    assert response_3.status_code == 401
    assert response_3.json() == {'detail': 'Unauthorized'}

    headers4 = add_authorization_header(token1.key, headers)
    url4 = admin_job_urls.Job_Single_Url.format('any-values-this')
    response_4 = await async_client.get(url=url4, headers=headers4)
    assert response_4.status_code == 422

    headers5 = add_authorization_header(token1.key, headers)
    url5 = admin_job_urls.Job_Single_Url.format('11111111-1111-1111-1111-111111111111')
    response_5 = await async_client.get(url=url5, headers=headers5)
    assert response_5.status_code == 404
    assert response_5.json() == {'detail': 'The job item `11111111-1111-1111-1111-111111111111` is not found'}

    url6 = admin_job_urls.Job_Single_Url.format(job_1['id'])
    response_6 = await async_client.get(url=url6, headers=headers)
    assert response_6.status_code == 401
    assert response_6.json() == {'detail': 'Unauthorized'}


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()

