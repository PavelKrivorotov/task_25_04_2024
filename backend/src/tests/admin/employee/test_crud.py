import uuid
import datetime

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.utils import hash_password
from job.models import Job, UserJob
from admin.employee.crud import admin_employee_crud


class TestAdminEmployeeCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_retrieve(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('f1438d6f-09e6-4307-9353-a49e24cf4512'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        user_1 = {
            'id': uuid.UUID('dc72945b-42a2-4d88-99ec-8b2e83bffebe'),
            'username': 'admin-retrieve-employees-crud-admin1',
            'password': 'admin',
            'first_name': 'AdminRetrieveEmployeesCRUDAdmin1',
            'last_name': 'AdminRetrieveEmployeesCRUDAdmin1',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('34acba10-eac7-4b21-81b6-611112106679'),
            'username': 'admin-retrieve-employees-crud-user-1',
            'password': '9hdca',
            'first_name': 'AdminRetrieveEmployeesCRUDUser1',
            'last_name': 'AdminRetrieveEmployeesCRUDUser1',
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
            'id': uuid.UUID('ef1d135d-1b1d-441c-bc59-591d60360d65'),
            'job_id': uuid.UUID('f1438d6f-09e6-4307-9353-a49e24cf4512'),
            'user_id': uuid.UUID('34acba10-eac7-4b21-81b6-611112106679')
        }

        user_job2 = UserJob(**user_job_2)
        db_session.add(user_job2)
        await db_session.commit()

        json_result = {
            'user': {
                'id': '34acba10-eac7-4b21-81b6-611112106679',
                'username': 'admin-retrieve-employees-crud-user-1',
                'first_name': 'AdminRetrieveEmployeesCRUDUser1',
                'last_name': 'AdminRetrieveEmployeesCRUDUser1',
                'date_of_employment': '2024-05-02',
                'is_staff': True,
                'is_superuser': False
            },
            'job': {
                'id': 'f1438d6f-09e6-4307-9353-a49e24cf4512',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            }
        }

        employee1 = await admin_employee_crud.retrieve(db_session, str(user_2['id']))
        assert employee1 == json_result


        # clear db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_list(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('e85755c0-d6a9-44ce-afc6-e0a542faba8b'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }
        job_2 = {
            'id': uuid.UUID('0233cbf0-d8d9-48c4-b6a2-ed1ffd133bbc'),
            'title': 'Junior python developer',
            'salary': 50000,
            'days_to_promotion': datetime.timedelta(days=365)
        }

        user_1 = {
            'id': uuid.UUID('aa678fdd-301c-4d34-b570-adaca4ac8928'),
            'username': 'admin-list-employees-crud-admin1',
            'password': 'admin',
            'first_name': 'AdminListEmployeesCRUDAdmin1',
            'last_name': 'AdminListEmployeesCRUDAdmin1',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('7e92c31a-45ec-447d-af92-ae0d9b65c16b'),
            'username': 'admin-list-employees-crud-user-1',
            'password': '9hdca',
            'first_name': 'AdminListEmployeesCRUDUser1',
            'last_name': 'AdminListEmployeesCRUDUser1',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': True,
            'is_superuser': False
        }
        user_3 = {
            'id': uuid.UUID('8eeafec2-85b7-448b-a0a7-757e0b9366a7'),
            'username': 'admin-list-employees-crud-user-2',
            'password': '4esef',
            'first_name': 'AdminListEmployeesCRUDUser2',
            'last_name': 'AdminListEmployeesCRUDUser2',
            'date_of_employment': datetime.date(year=2024, month=5, day=2),
            'is_staff': True,
            'is_superuser': False
        }
        user_4 = {
            'id': uuid.UUID('99b6a25b-2c4c-41ea-899e-bc2a63465a7d'),
            'username': 'admin-list-employees-crud-user-3',
            'password': '8yhwdio',
            'first_name': 'AdminListEmployeesCRUDUser3',
            'last_name': 'AdminListEmployeesCRUDUser3',
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
            'id': uuid.UUID('1ee7db83-51e6-470a-abda-047b522ca187'),
            'job_id': uuid.UUID('e85755c0-d6a9-44ce-afc6-e0a542faba8b'),
            'user_id': uuid.UUID('7e92c31a-45ec-447d-af92-ae0d9b65c16b')
        }
        user_job_3 = {
            'id': uuid.UUID('a3f603ee-ae73-4968-a453-344ecb4f552f'),
            'job_id': uuid.UUID('e85755c0-d6a9-44ce-afc6-e0a542faba8b'),
            'user_id': uuid.UUID('8eeafec2-85b7-448b-a0a7-757e0b9366a7')
        }
        user_job_4 = {
            'id': uuid.UUID('d49a0518-f187-4369-975c-a57f05337ef2'),
            'job_id': uuid.UUID('0233cbf0-d8d9-48c4-b6a2-ed1ffd133bbc'),
            'user_id': uuid.UUID('99b6a25b-2c4c-41ea-899e-bc2a63465a7d')
        }

        user_job2 = UserJob(**user_job_2)
        user_job3 = UserJob(**user_job_3)
        user_job4 = UserJob(**user_job_4)

        db_session.add_all([user_job2, user_job3, user_job4])
        await db_session.commit()

        json_result = {
            'count': 3,
            'results': [
                {
                    'user': {
                        'id': '7e92c31a-45ec-447d-af92-ae0d9b65c16b',
                        'username': 'admin-list-employees-crud-user-1',
                        'first_name': 'AdminListEmployeesCRUDUser1',
                        'last_name': 'AdminListEmployeesCRUDUser1',
                        'date_of_employment': '2024-05-02',
                        'is_staff': True,
                        'is_superuser': False
                    },
                    'job': {
                        'id': 'e85755c0-d6a9-44ce-afc6-e0a542faba8b',
                        'title': 'Intern python developer',
                        'salary': 20000,
                        'days_to_promotion': 180
                    }
                },
                {
                    'user': {
                        'id': '8eeafec2-85b7-448b-a0a7-757e0b9366a7',
                        'username': 'admin-list-employees-crud-user-2',
                        'first_name': 'AdminListEmployeesCRUDUser2',
                        'last_name': 'AdminListEmployeesCRUDUser2',
                        'date_of_employment': '2024-05-02',
                        'is_staff': True,
                        'is_superuser': False
                    },
                    'job': {
                        'id': 'e85755c0-d6a9-44ce-afc6-e0a542faba8b',
                        'title': 'Intern python developer',
                        'salary': 20000,
                        'days_to_promotion': 180
                    }
                },
                {
                    'user': {
                        'id': '99b6a25b-2c4c-41ea-899e-bc2a63465a7d',
                        'username': 'admin-list-employees-crud-user-3',
                        'first_name': 'AdminListEmployeesCRUDUser3',
                        'last_name': 'AdminListEmployeesCRUDUser3',
                        'date_of_employment': '2024-05-02',
                        'is_staff': True,
                        'is_superuser': False
                    },
                    'job': {
                        'id': '0233cbf0-d8d9-48c4-b6a2-ed1ffd133bbc',
                        'title': 'Junior python developer',
                        'salary': 50000,
                        'days_to_promotion': 365
                    }
                }
            ]
        }

        result1 = await admin_employee_crud.list(db_session)
        assert result1 == json_result


        # clear db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()

