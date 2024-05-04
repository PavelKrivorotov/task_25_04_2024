import uuid
import datetime
from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User, Token
from auth.utils import hash_password
from job.models import Job, UserJob
from admin.employee import urls as admin_employee_url

from tests.utils import add_authorization_header


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_list_employees(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('64d56cb2-26d4-498f-901b-fb3627556935'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('2b8f891a-fb53-42a9-abde-5049e05120d4'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }

    user_1 = {
        'id': uuid.UUID('efffbe1c-a2d4-47db-ba6b-d8ed0f57d402'),
        'username': 'admin-list-employees-admin1',
        'password': 'admin',
        'first_name': 'AdminListEmployeesAdmin1',
        'last_name': 'AdminListEmployeesAdmin1',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('568add16-b853-481a-bb32-982e4741f9d4'),
        'username': 'admin-list-employees-user-1',
        'password': '9hdca',
        'first_name': 'AdminListEmployeesUser1',
        'last_name': 'AdminListEmployeesUser1',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': True,
        'is_superuser': False
    }
    user_3 = {
        'id': uuid.UUID('b1ebbdaf-8582-4dbd-83b6-14fe52915dc3'),
        'username': 'admin-list-employees-user-2',
        'password': '4esef',
        'first_name': 'AdminListEmployeesUser2',
        'last_name': 'AdminListEmployeesUser2',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': True,
        'is_superuser': False
    }
    user_4 = {
        'id': uuid.UUID('c5348556-a634-4e51-aff2-c415da8d6a09'),
        'username': 'admin-list-employees-user-3',
        'password': '8yhwdio',
        'first_name': 'AdminListEmployeesUser3',
        'last_name': 'AdminListEmployeesUser3',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
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

    u4 = user_4.copy()
    u4['password'] = hash_password(u4['password'])
    user4 = User(**u4)

    db_session.add_all([job1, job2, user1, user2, user3, user4])
    await db_session.commit()

    user_job_2 = {
        'id': uuid.UUID('590acb6e-a5d6-45ec-a48f-af7a5566842e'),
        'job_id': uuid.UUID('64d56cb2-26d4-498f-901b-fb3627556935'),
        'user_id': uuid.UUID('568add16-b853-481a-bb32-982e4741f9d4')
    }
    user_job_3 = {
        'id': uuid.UUID('d3bd4f34-8774-4f19-bc9d-96870c286188'),
        'job_id': uuid.UUID('64d56cb2-26d4-498f-901b-fb3627556935'),
        'user_id': uuid.UUID('b1ebbdaf-8582-4dbd-83b6-14fe52915dc3')
    }
    user_job_4 = {
        'id': uuid.UUID('59cf9412-92d5-42e4-8993-6eca5490c855'),
        'job_id': uuid.UUID('2b8f891a-fb53-42a9-abde-5049e05120d4'),
        'user_id': uuid.UUID('c5348556-a634-4e51-aff2-c415da8d6a09')
    }

    token_1 = {
        'key': '155a01d067e30137e681a40adaa0df8277b3aa4485ff457c',
        'user_id': uuid.UUID('efffbe1c-a2d4-47db-ba6b-d8ed0f57d402')
    }
    token_2 = {
        'key': '469449be93462dfdad3f77b2e9f1dda4393f69965839470c',
        'user_id': uuid.UUID('568add16-b853-481a-bb32-982e4741f9d4')
    }

    user_job2 = UserJob(**user_job_2)
    user_job3 = UserJob(**user_job_3)
    user_job4 = UserJob(**user_job_4)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, user_job3, user_job4, token1, token2])
    await db_session.commit()

    json_result = {
        'count': 3,
        'results': [
            {
                'user': {
                    'id': '568add16-b853-481a-bb32-982e4741f9d4',
                    'username': 'admin-list-employees-user-1',
                    'first_name': 'AdminListEmployeesUser1',
                    'last_name': 'AdminListEmployeesUser1',
                    'date_of_employment': '2024-05-02',
                    'is_staff': True,
                    'is_superuser': False
                },
                'job': {
                    'id': '64d56cb2-26d4-498f-901b-fb3627556935',
                    'title': 'Intern python developer',
                    'salary': 20000,
                    'days_to_promotion': 180
                }
            },
            {
                'user': {
                    'id': 'b1ebbdaf-8582-4dbd-83b6-14fe52915dc3',
                    'username': 'admin-list-employees-user-2',
                    'first_name': 'AdminListEmployeesUser2',
                    'last_name': 'AdminListEmployeesUser2',
                    'date_of_employment': '2024-05-02',
                    'is_staff': True,
                    'is_superuser': False
                },
                'job': {
                    'id': '64d56cb2-26d4-498f-901b-fb3627556935',
                    'title': 'Intern python developer',
                    'salary': 20000,
                    'days_to_promotion': 180
                }
            },
            {
                'user': {
                    'id': 'c5348556-a634-4e51-aff2-c415da8d6a09',
                    'username': 'admin-list-employees-user-3',
                    'first_name': 'AdminListEmployeesUser3',
                    'last_name': 'AdminListEmployeesUser3',
                    'date_of_employment': '2024-05-02',
                    'is_staff': True,
                    'is_superuser': False
                },
                'job': {
                    'id': '2b8f891a-fb53-42a9-abde-5049e05120d4',
                    'title': 'Junior python developer',
                    'salary': 50000,
                    'days_to_promotion': 365
                }
            }
        ]
    }

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.get(url=admin_employee_url.Employees_List_Url, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_result

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.get(url=admin_employee_url.Employees_List_Url, headers=headers2)
    assert response_2.status_code == 403
    assert response_2.json() == {'detail': 'Invalid permissions. Allowed only `Admin`'}

    headers3 = add_authorization_header('fake-access-token-key', headers)
    response_3 = await async_client.get(url=admin_employee_url.Employees_List_Url, headers=headers3)
    assert response_3.status_code == 401
    assert response_3.json() == {'detail': 'Unauthorized'}

    response_4 = await async_client.get(url=admin_employee_url.Employees_List_Url, headers=headers)
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
async def test_retrieve_employees(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('8b27554c-c108-4634-9fda-f0c5bf62fa6c'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    user_1 = {
        'id': uuid.UUID('55859aa1-8c62-45f0-9bbd-7d23e8678f3a'),
        'username': 'admin-retrieve-employees-admin1',
        'password': 'admin',
        'first_name': 'AdminRetrieveEmployeesAdmin1',
        'last_name': 'AdminRetrieveEmployeesAdmin1',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('f306c681-7813-43c9-b940-fecf0a7514cc'),
        'username': 'admin-retrieve-employees-user-1',
        'password': '9hdca',
        'first_name': 'AdminRetrieveEmployeesUser1',
        'last_name': 'AdminRetrieveEmployeesUser1',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
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
        'id': uuid.UUID('fecb7253-5b49-4745-82cc-f6142c99ed70'),
        'job_id': uuid.UUID('8b27554c-c108-4634-9fda-f0c5bf62fa6c'),
        'user_id': uuid.UUID('f306c681-7813-43c9-b940-fecf0a7514cc')
    }

    token_1 = {
        'key': '1dd1a310d1d2d54be94d8a028c979b171f6dce282fc33f24',
        'user_id': uuid.UUID('55859aa1-8c62-45f0-9bbd-7d23e8678f3a')
    }
    token_2 = {
        'key': '5a719d8e5f525767bbbc3b7e1cf7807e36ef2a4950a64143',
        'user_id': uuid.UUID('f306c681-7813-43c9-b940-fecf0a7514cc')
    }

    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)

    db_session.add_all([user_job2, token1, token2])
    await db_session.commit()

    json_result = {
        'user': {
            'id': 'f306c681-7813-43c9-b940-fecf0a7514cc',
            'username': 'admin-retrieve-employees-user-1',
            'first_name': 'AdminRetrieveEmployeesUser1',
            'last_name': 'AdminRetrieveEmployeesUser1',
            'date_of_employment': '2024-05-02',
            'is_staff': True,
            'is_superuser': False
        },
        'job': {
            'id': '8b27554c-c108-4634-9fda-f0c5bf62fa6c',
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': 180
        }
    }

    headers1 = add_authorization_header(token1.key, headers)
    url1 = admin_employee_url.Employees_Single_Url.format(user_2['id'])
    response_1 = await async_client.get(url=url1, headers=headers1)
    assert response_1.status_code == 200
    assert response_1.json() == json_result

    headers2 = add_authorization_header(token1.key, headers)
    url2 = admin_employee_url.Employees_Single_Url.format(user_1['id'])
    response_2 = await async_client.get(url=url2, headers=headers2)
    assert response_2.status_code == 403
    assert response_2.json() == {'detail': 'Information about `Admin` is not allowed'}

    headers3 = add_authorization_header(token2.key, headers)
    url3 = admin_employee_url.Employees_Single_Url.format(user_2['id'])
    response_3 = await async_client.get(url=url3, headers=headers3)
    assert response_3.status_code == 403
    assert response_3.json() == {'detail': 'Invalid permissions. Allowed only `Admin`'}

    url4 = admin_employee_url.Employees_Single_Url.format(user_2['id'])
    response_4 = await async_client.get(url=url3, headers=headers)
    assert response_4.status_code == 401
    assert response_4.json() == {'detail': 'Unauthorized'}


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()

