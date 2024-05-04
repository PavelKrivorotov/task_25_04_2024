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
async def test_me(
    async_client: AsyncClient,
    db_session: AsyncSession,
    headers: dict[str, Any],
):
    job_1 = {
        'id': uuid.UUID('e58c423c-06a9-42b8-a475-b23467e8e150'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('b1fb923c-84bd-4bdf-9498-194d761f755a'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }

    user_1 = {
        'id': uuid.UUID('f87c04ab-1158-4b27-89b7-73c61770be15'),
        'username': 'me-admin1',
        'password': 'admin',
        'first_name': 'MeAdmin1',
        'last_name': 'MeAdmin1',
        'date_of_employment': datetime.date(2024,5, 2),
        'is_staff': False,
        'is_superuser': True
    }
    user_2 = {
        'id': uuid.UUID('c08a24d3-b7d1-46a0-9461-fb20c1e78b2f'),
        'username': 'me-user-1',
        'password': 'g6e3d',
        'first_name': 'MeUser1',
        'last_name': 'MeUser2',
        'date_of_employment': datetime.date(2024,5, 2),
        'is_staff': True,
        'is_superuser': False
    }
    user_3 = {
        'id': uuid.UUID('0da6110e-49e9-4336-8d3c-ae11acdc7486'),
        'username': 'me-user-2',
        'password': '9ej3d',
        'first_name': 'MeUser2',
        'last_name': 'MeUser3',
        'date_of_employment': datetime.date(2024,5, 2),
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
        'id': uuid.UUID('bae92237-3628-4ee9-a619-88c8cff2f2d6'),
        'job_id': uuid.UUID('e58c423c-06a9-42b8-a475-b23467e8e150'),
        'user_id': uuid.UUID('c08a24d3-b7d1-46a0-9461-fb20c1e78b2f')
    }
    user_job_2 = {
        'id': uuid.UUID('fd12fb19-cfb1-4044-b2f4-67050653562f'),
        'job_id': uuid.UUID('b1fb923c-84bd-4bdf-9498-194d761f755a'),
        'user_id': uuid.UUID('0da6110e-49e9-4336-8d3c-ae11acdc7486')
    }

    token_1 = {
        'key': '0d2b247c3d2f438876c6209d1204f7701659cd4c78125d65',
        'user_id': uuid.UUID('f87c04ab-1158-4b27-89b7-73c61770be15')
    }
    token_2 = {
        'key': 'b200f3f2088a81fea7997812e4b0bfad2c52e000ebb7a0e7',
        'user_id': uuid.UUID('c08a24d3-b7d1-46a0-9461-fb20c1e78b2f')
    }
    token_3= {
        'key': '8984a1f74692e44477891d945b438ca2b285666f8dbc18c4',
        'user_id': uuid.UUID('0da6110e-49e9-4336-8d3c-ae11acdc7486')
    }

    user_job1 = UserJob(**user_job_1)
    user_job2 = UserJob(**user_job_2)

    token1 = Token(**token_1)
    token2 = Token(**token_2)
    token3 = Token(**token_3)

    db_session.add_all([user_job1, user_job2, token1, token2, token3])
    await db_session.commit()

    headers1 = add_authorization_header(token1.key, headers)
    response_1 = await async_client.get(employee_urls.Me_Url, headers=headers1)
    assert response_1.status_code == 403
    assert response_1.json() == {'detail': 'Invalid permissions. Allowed only `Staff`'}

    headers2 = add_authorization_header(token2.key, headers)
    response_2 = await async_client.get(employee_urls.Me_Url, headers=headers2)
    assert response_2.status_code == 200
    assert response_2.json() == {
        'user': {
            'id': 'c08a24d3-b7d1-46a0-9461-fb20c1e78b2f',
            'username': 'me-user-1',
            'first_name': 'MeUser1',
            'last_name': 'MeUser2',
            'date_of_employment': '2024-05-02',
            'is_staff': True,
            'is_superuser': False
        },
        'job': get_external_url_to_route(job_urls.Me_Url)
    }

    headers3 = add_authorization_header(token3.key, headers)
    response_3 = await async_client.get(employee_urls.Me_Url, headers=headers3)
    assert response_3.status_code == 200
    assert response_3.json() == {
        'user': {
            'id': '0da6110e-49e9-4336-8d3c-ae11acdc7486',
            'username': 'me-user-2',
            'first_name': 'MeUser2',
            'last_name': 'MeUser3',
            'date_of_employment': '2024-05-02',
            'is_staff': True,
            'is_superuser': False
        },
        'job': get_external_url_to_route(job_urls.Me_Url)
    }

    fake_token = 'fake-authorization-token'
    headers4 = add_authorization_header(fake_token, headers)
    response_4 = await async_client.get(employee_urls.Me_Url, headers=headers4)
    assert response_4.status_code == 401
    assert response_4.json() == {'detail': 'Unauthorized'}

    headers5 = headers
    response_5 = await async_client.get(employee_urls.Me_Url, headers=headers5)
    assert response_5.status_code == 401
    assert response_5.json() == {'detail': 'Unauthorized'}


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.execute(delete(Token))
    await db_session.commit()

