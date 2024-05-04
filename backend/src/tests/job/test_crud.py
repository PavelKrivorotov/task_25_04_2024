import uuid
import datetime

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_external_url_to_route
from auth.models import User
from auth.utils import hash_password

from employee import urls as employee_urls

from job.models import Job, UserJob
from job.crud import job_crud


class TestJobCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_me(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('3faafcc9-96ed-44e1-ab22-fa2031ba773a'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        user_1 = {
            'id': uuid.UUID('5dc5d7da-6bfe-4ddd-a005-332ab7e963e3'),
            'username': 'me-job-crud-admin1',
            'password': 'admin',
            'first_name': 'MeJobCRUDAdmin1',
            'last_name': 'MeJobCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('be7318a1-22e9-4168-a4ec-94e95ad91e83'),
            'username': 'me-job-crud-user1',
            'password': '8yu2gsd',
            'first_name': 'MeJobCRUDUser1',
            'last_name': 'MeJobCRUDUser1',
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
            'id': uuid.UUID('fc281616-241f-4e55-b296-80254eabe2bb'),
            'job_id': uuid.UUID('3faafcc9-96ed-44e1-ab22-fa2031ba773a'),
            'user_id': uuid.UUID('be7318a1-22e9-4168-a4ec-94e95ad91e83')
        }

        user_job2 = UserJob(**user_job_2)
        db_session.add(user_job2)
        await db_session.commit()

        with pytest.raises(AttributeError):
            response_1 = await job_crud.me(db_session, user1)

        response_2 = await job_crud.me(db_session, user2)
        assert response_2 == {
            'user': get_external_url_to_route(employee_urls.Me_Url),
            'job': {
                'id': str(job_1['id']),
                'title': job_1['title'],
                'salary': job_1['salary'],
                'days_to_promotion': job_1['days_to_promotion'].days
            }
        }


        # cleae db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_retrieve(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('19e628b2-88a9-416e-ab7b-9ea2e129b10d'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }

        user_1 = {
            'id': uuid.UUID('2b4bc484-80a1-43a1-a596-6e710e7dbec7'),
            'username': 'retrieve-job-crud-admin1',
            'password': 'admin',
            'first_name': 'RetrieveJobCRUDAdmin1',
            'last_name': 'RetrieveJobCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('c2d79dd6-ebdc-4e54-8311-8814cb5b2c45'),
            'username': 'retrirve-job-crud-user1',
            'password': '765w',
            'first_name': 'RetrieveJobCRUDUser1',
            'last_name': 'RetrieveJobCRUDUser1',
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
            'id': uuid.UUID('4deffc71-7a6b-4460-b898-27adb931da62'),
            'job_id': uuid.UUID('19e628b2-88a9-416e-ab7b-9ea2e129b10d'),
            'user_id': uuid.UUID('c2d79dd6-ebdc-4e54-8311-8814cb5b2c45')
        }

        user_job2 = UserJob(**user_job_2)
        db_session.add(user_job2)
        await db_session.commit()

        response_1 = await job_crud.retrieve(job1, user1)
        assert response_1 == {
            'job': {
                'id': '19e628b2-88a9-416e-ab7b-9ea2e129b10d',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            }
        }

        response_2 = await job_crud.retrieve(job1, user2)
        assert response_2 == {
            'job': {
                'id': '19e628b2-88a9-416e-ab7b-9ea2e129b10d',
                'title': 'Intern python developer'
            }
        }

        response_3 = await job_crud.retrieve(job1)
        assert response_3 == {
            'job': {
                'id': '19e628b2-88a9-416e-ab7b-9ea2e129b10d',
                'title': 'Intern python developer'
            }
        }


        # cleae db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()


    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_list(self, db_session: AsyncSession):
        job_1 = {
            'id': uuid.UUID('4ea61b6a-2321-4a10-821e-1e995575ea12'),
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }
        job_2 = {
            'id': uuid.UUID('bb8a1648-d1ca-45f4-9d7d-604232e2be30'),
            'title': 'Junior python developer',
            'salary': 50000,
            'days_to_promotion': datetime.timedelta(days=365)
        }
        job_3 = {
            'id': uuid.UUID('c3d6eed2-b978-47fc-94ed-fbe9ecf20b42'),
            'title': 'Middle python developer',
            'salary': 120000,
            'days_to_promotion': datetime.timedelta(days=540)
        }

        user_1 = {
            'id': uuid.UUID('309294de-5fe8-4e8a-ab3e-23ed464cda43'),
            'username': 'list-jobs-crud-admin1',
            'password': 'admin',
            'first_name': 'ListJobsCRUDAdmin1',
            'last_name': 'ListJobsCRUDAdmin1',
            'is_staff': False,
            'is_superuser': True
        }
        user_2 = {
            'id': uuid.UUID('79ba57be-7045-47b7-afa8-cdbcc345fdda'),
            'username': 'list-jobs-crud-user-1',
            'password': '7wtg2s',
            'first_name': 'ListJobsCRUDUser1',
            'last_name': 'ListJobsCRUDUser2',
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
            'id': uuid.UUID('b3ffa422-1f41-4b2c-8ca2-b47d3053c663'),
            'job_id': uuid.UUID('4ea61b6a-2321-4a10-821e-1e995575ea12'),
            'user_id': uuid.UUID('79ba57be-7045-47b7-afa8-cdbcc345fdda')
        }

        user_job2 = UserJob(**user_job_2)
        db_session.add(user_job2)
        await db_session.commit()

        extend_json_result = {
            'count': 3,
            'results': [
                {
                    'id': '4ea61b6a-2321-4a10-821e-1e995575ea12',
                    'title': 'Intern python developer',
                    'salary': 20000,
                    'days_to_promotion': 180
                },
                {
                    'id': 'bb8a1648-d1ca-45f4-9d7d-604232e2be30',
                    'title': 'Junior python developer',
                    'salary': 50000,
                    'days_to_promotion': 365
                },
                {
                    'id': 'c3d6eed2-b978-47fc-94ed-fbe9ecf20b42',
                    'title': 'Middle python developer',
                    'salary': 120000,
                    'days_to_promotion': 540
                }
            ]
        }

        json_result = {
            'count': 3,
            'results' : [
                {
                    'id': '4ea61b6a-2321-4a10-821e-1e995575ea12',
                    'title': 'Intern python developer',
                },
                {
                    'id': 'bb8a1648-d1ca-45f4-9d7d-604232e2be30',
                    'title': 'Junior python developer',
                },
                {
                    'id': 'c3d6eed2-b978-47fc-94ed-fbe9ecf20b42',
                    'title': 'Middle python developer',
                }
            ]
        }

        response_1 = await job_crud.list(db_session, user1)
        assert response_1 == extend_json_result

        response_2 = await job_crud.list(db_session, user2)
        assert response_2 == json_result

        response_3 = await job_crud.list(db_session)
        assert response_3 == json_result


        # clear db
        await db_session.execute(delete(Job))
        await db_session.execute(delete(User))
        await db_session.execute(delete(UserJob))
        await db_session.commit()

