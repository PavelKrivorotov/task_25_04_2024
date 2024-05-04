import uuid
import datetime

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.utils import hash_password
from job.models import Job, UserJob

from admin.employee.queries import query as q
from admin.employee.converters import convert_employee


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio()
async def test_convert_employee(db_session: AsyncSession):
    job_1 = {
        'id': uuid.UUID('c8825d57-a3d4-447e-a1c3-dbe6eaef2481'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }
    job_2 = {
        'id': uuid.UUID('835eebd9-943e-43d1-a4c2-2e0870ecd129'),
        'title': 'Junior python developer',
        'salary': 50000,
        'days_to_promotion': datetime.timedelta(days=365)
    }

    user_2 = {
        'id': uuid.UUID('59b47157-6168-449c-b627-ee69b7930e07'),
        'username': 'admin-list-employees-converters-user-1',
        'password': '9hdca',
        'first_name': 'AdminListEmployeesCRUDUser1',
        'last_name': 'AdminListEmployeesCRUDUser1',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': True,
        'is_superuser': False
    }
    user_3 = {
        'id': uuid.UUID('7c205f60-7b54-403e-a39b-02fed619e1a4'),
        'username': 'admin-list-employees-converters-user-2',
        'password': '4esef',
        'first_name': 'AdminListEmployeesCRUDUser2',
        'last_name': 'AdminListEmployeesCRUDUser2',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': True,
        'is_superuser': False
    }
    user_4 = {
        'id': uuid.UUID('86591443-7aaa-4a2a-ad00-647bae05f42e'),
        'username': 'admin-list-employees-converters-user-3',
        'password': '8yhwdio',
        'first_name': 'AdminListEmployeesCRUDUser3',
        'last_name': 'AdminListEmployeesCRUDUser3',
        'date_of_employment': datetime.date(year=2024, month=5, day=2),
        'is_staff': True,
        'is_superuser': False
    }

    job1 = Job(**job_1)
    job2 = Job(**job_2)

    u2 = user_2.copy()
    u2['password'] = hash_password(u2['password'])
    user2 = User(**u2)

    u3 = user_3.copy()
    u3['password'] = hash_password(u3['password'])
    user3 = User(**u3)

    u4 = user_4.copy()
    u4['password'] = hash_password(u4['password'])
    user4 = User(**u4)

    db_session.add_all([job1, job2, user2, user3, user4])
    await db_session.commit()

    user_job_2 = {
        'id': uuid.UUID('8b40a016-18bd-4b1a-a145-78fd21eb1fae'),
        'job_id': uuid.UUID('c8825d57-a3d4-447e-a1c3-dbe6eaef2481'),
        'user_id': uuid.UUID('59b47157-6168-449c-b627-ee69b7930e07')
    }
    user_job_3 = {
        'id': uuid.UUID('804af11c-df34-4d64-b8b9-50b4e62ee05d'),
        'job_id': uuid.UUID('c8825d57-a3d4-447e-a1c3-dbe6eaef2481'),
        'user_id': uuid.UUID('7c205f60-7b54-403e-a39b-02fed619e1a4')
    }
    user_job_4 = {
        'id': uuid.UUID('f288fad5-8ddf-49b5-bb43-f01f9734fb10'),
        'job_id': uuid.UUID('835eebd9-943e-43d1-a4c2-2e0870ecd129'),
        'user_id': uuid.UUID('86591443-7aaa-4a2a-ad00-647bae05f42e')
    }

    user_job2 = UserJob(**user_job_2)
    user_job3 = UserJob(**user_job_3)
    user_job4 = UserJob(**user_job_4)

    db_session.add_all([user_job2, user_job3, user_job4])
    await db_session.commit()

    convert_result = [
        {
            'user_id': uuid.UUID('59b47157-6168-449c-b627-ee69b7930e07'),
            'username': 'admin-list-employees-converters-user-1',
            'first_name': 'AdminListEmployeesCRUDUser1',
            'last_name': 'AdminListEmployeesCRUDUser1',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': True,
            'is_superuser': False,
            'job_id': uuid.UUID('c8825d57-a3d4-447e-a1c3-dbe6eaef2481'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        },
        {
            'user_id': uuid.UUID('7c205f60-7b54-403e-a39b-02fed619e1a4'),
            'username': 'admin-list-employees-converters-user-2',
            'first_name': 'AdminListEmployeesCRUDUser2',
            'last_name': 'AdminListEmployeesCRUDUser2',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': True,
            'is_superuser': False,
            'job_id': uuid.UUID('c8825d57-a3d4-447e-a1c3-dbe6eaef2481'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        },
        {
            'user_id': uuid.UUID('86591443-7aaa-4a2a-ad00-647bae05f42e'),
            'username': 'admin-list-employees-converters-user-3',
            'first_name': 'AdminListEmployeesCRUDUser3',
            'last_name': 'AdminListEmployeesCRUDUser3',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': True,
            'is_superuser': False,
            'job_id': uuid.UUID('835eebd9-943e-43d1-a4c2-2e0870ecd129'),
            'title': 'Junior python developer',
            'salary': 50000,
            'days_to_promotion': datetime.timedelta(days=365)
        }
    ]

    query = q.order_by(User.id)
    result = await db_session.execute(query)

    res = convert_employee(result)
    assert res == convert_result


    # clear db
    await db_session.execute(delete(Job))
    await db_session.execute(delete(User))
    await db_session.execute(delete(UserJob))
    await db_session.commit()

