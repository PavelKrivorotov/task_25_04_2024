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

from employee import urls as employee_urls
from job import urls as job_urls
from job.models import Job, UserJob

from tests.utils import add_authorization_header


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_my_job(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('637a7f5c-90f6-4e92-95f5-c5e28db7379d'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    user_1 = {
        'id': uuid.UUID('cd08e3d9-679d-4c98-8cf2-a405a475e66e'),
        'username': 'my-job-admin1',
        'password': 'admin',
        'first_name': 'MyJobAdmin1',
        'last_name': 'MyJobAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('f34a1b35-a944-45ce-8579-6dde5de2ace4'),
        'username': 'my-job-user-1',
        'password': '8ye62f',
        'first_name': 'MyJobUser1',
        'last_name': 'MyJobUser2',
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
        'id': uuid.UUID('3cc2ebcf-7ab3-4a55-a0d2-68d6a84f51ab'),
        'job_id': uuid.UUID('637a7f5c-90f6-4e92-95f5-c5e28db7379d'),
        'user_id': uuid.UUID('f34a1b35-a944-45ce-8579-6dde5de2ace4')
    }

    token_1 = {
        'key': '122d5506e7a8901ee23a0544f19ea0871bf6e7d515625cb1',
        'user_id': uuid.UUID('cd08e3d9-679d-4c98-8cf2-a405a475e66e')
    }
    token_2 = {
        'key': '009f67a0680d3b3994b708eeee5e84187e363d722a90605d',
        'user_id': uuid.UUID('f34a1b35-a944-45ce-8579-6dde5de2ace4')
    }

    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.get(url=job_urls.Me_Url, headers=headers1)
    assert response_1.status_code == 403
    assert response_1.json() == {'detail': 'Invalid permissions. Allowed only `Staff`'}

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.get(url=job_urls.Me_Url, headers=headers2)
    assert response_2.status_code == 200
    assert response_2.json() == {
        'user': get_external_url_to_route(employee_urls.Me_Url),
        'job': {
            'id': '637a7f5c-90f6-4e92-95f5-c5e28db7379d',
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': 180
        }
    }

    headers3 = add_authorization_header('fake-access-token-key', headers)
    response_3 = await async_client.get(url=job_urls.Me_Url, headers=headers3)
    assert response_3.status_code == 401
    assert response_3.json() == {'detail': 'Unauthorized'}


    # cleaer database
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
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
        'id': uuid.UUID('1adc1a0c-f76f-48e6-bf9a-a573e33cbe38'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('5a9c2471-fd5e-45e2-95fb-b4a38b09a1eb'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }
    job_3 = {
        'id': uuid.UUID('f8ff02d4-fb7f-45a0-b33f-dce03cf5b6bc'),
        'title': 'Middle python developer',
        'salary': 120000,
        'days_to_promotion': datetime.timedelta(days=540)
    }

    user_1 = {
        'id': uuid.UUID('9d3cdd90-bf26-4dd1-9e48-6eec3ff7672f'),
        'username': 'list-jobs-admin1',
        'password': 'admin',
        'first_name': 'ListJobsAdmin1',
        'last_name': 'ListJobsAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('de837978-23ce-4983-92da-c9ec037ff978'),
        'username': 'list-jobs-user-1',
        'password': '92ye7',
        'first_name': 'ListJobsUser1',
        'last_name': 'ListJobsUser2',
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
        'id': uuid.UUID('83159bf5-6fae-4855-93ef-ae9eb127c027'),
        'job_id': uuid.UUID('1adc1a0c-f76f-48e6-bf9a-a573e33cbe38'),
        'user_id': uuid.UUID('de837978-23ce-4983-92da-c9ec037ff978')
    }

    token_1 = {
        'key': '9ee162ec3041c32991666069366cef433f9a7f07a07893bd',
        'user_id': uuid.UUID('9d3cdd90-bf26-4dd1-9e48-6eec3ff7672f')
    }
    token_2 = {
        'key': 'e35921898c2dfed51c4adeb90c7684dbfd14f6f96056152d',
        'user_id': uuid.UUID('de837978-23ce-4983-92da-c9ec037ff978')
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
                'id': '1adc1a0c-f76f-48e6-bf9a-a573e33cbe38',
                'title': 'Intern python developer'
            },
            {
                'id': '5a9c2471-fd5e-45e2-95fb-b4a38b09a1eb',
                'title': 'Junior python developer'
            },
            {
                'id': 'f8ff02d4-fb7f-45a0-b33f-dce03cf5b6bc',
                'title': 'Middle python developer'
            }
        ]
    }

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.get(url=job_urls.Job_All_Url, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_result

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.get(url=job_urls.Job_All_Url, headers=headers2)
    assert response_2.status_code == 200
    assert response_2.json() == json_result

    headers3 = add_authorization_header('fake-access-token-key', headers)
    response_3 = await async_client.get(url=job_urls.Job_All_Url, headers=headers3)
    assert response_3.status_code == 200
    assert response_3.json() == json_result

    response_4 = await async_client.get(url=job_urls.Job_All_Url, headers=headers)
    assert response_4.status_code == 200
    assert response_4.json() == json_result


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
        'id': uuid.UUID('05a543ed-087a-465d-8222-f1ab23eefe1f'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    user_1 = {
        'id': uuid.UUID('0a73954f-a20b-4c74-9921-6b1664065393'),
        'username': 'single-jobs-admin1',
        'password': 'admin',
        'first_name': 'SingleJobsAdmin1',
        'last_name': 'SingleJobsAdmin1',
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('197be4b7-93ae-4f27-8091-22ad3c482dc2'),
        'username': 'single-jobs-user-1',
        'password': '128gsw',
        'first_name': 'SingleJobsUser1',
        'last_name': 'SingleJobsUser2',
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
        'id': uuid.UUID('b38c714f-4fc5-423d-97e3-c86ba4fe8d36'),
        'job_id': uuid.UUID('05a543ed-087a-465d-8222-f1ab23eefe1f'),
        'user_id': uuid.UUID('197be4b7-93ae-4f27-8091-22ad3c482dc2')
    }

    token_1 = {
        'key': 'c0db20cf6def3328c8413816b1867e6d732f456e7fcb02c4',
        'user_id': uuid.UUID('0a73954f-a20b-4c74-9921-6b1664065393')
    }
    token_2 = {
        'key': '4cc899f8468c9e3945780d05de3c6fc390ddfbfb80b7dfcc',
        'user_id': uuid.UUID('197be4b7-93ae-4f27-8091-22ad3c482dc2')
    }

    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    json_job = {
        'job': {
            'id': '05a543ed-087a-465d-8222-f1ab23eefe1f',
            'title': 'Intern python developer'
        }
    }

    headers1 = add_authorization_header(token1.key, headers)
    url1 = job_urls.Job_Single_Url.format(job_1['id'])
    response_1 = await async_client.get(url=url1, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_job

    headers2 = add_authorization_header(token2.key, headers)
    url2 = job_urls.Job_Single_Url.format(job_1['id'])
    response_2 = await async_client.get(url=url2, headers=headers2)
    assert response_2.status_code == 200
    assert response_2.json() == json_job

    headers3 = add_authorization_header('fake-access-token-key', headers)
    url3 = job_urls.Job_Single_Url.format(job_1['id'])
    response_3 = await async_client.get(url=url3, headers=headers3)
    assert response_3.status_code == 200
    assert response_3.json() == json_job

    headers4 = add_authorization_header(token1.key, headers)
    url4 = job_urls.Job_Single_Url.format('any-values-this')
    response_4 = await async_client.get(url=url4, headers=headers4)
    assert response_4.status_code == 422

    headers5 = add_authorization_header(token1.key, headers)
    url5 = job_urls.Job_Single_Url.format('11111111-1111-1111-1111-111111111111')
    response_5 = await async_client.get(url=url5, headers=headers5)
    assert response_5.status_code == 404
    assert response_5.json() == {'detail': 'The job item `11111111-1111-1111-1111-111111111111` is not found'}

    url6 = job_urls.Job_Single_Url.format(job_1['id'])
    response_6 = await async_client.get(url=url6, headers=headers)
    assert response_6.status_code == 200
    assert response_6.json() == json_job


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()

