import re

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import get_external_url_to_route
from job.models import Job
from admin.job import urls as admin_job_urls
from admin.job.schemas import CreateJob
from admin.job.crud import admin_job_crud


class TestAdminJobCRUD:
    @pytest.mark.asyncio(scope='session')
    # @pytest.mark.asyncio
    async def test_create(self, db_session: AsyncSession):
        job_1 = {
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': 180
        }

        data_job1 = CreateJob(**job_1)
        job1 = await admin_job_crud.create(db_session, data_job1)
        url_to_job = job1.get('job', None)
        assert isinstance(url_to_job, str)
        assert len(list(job1)) == 1

        url = get_external_url_to_route(admin_job_urls.Job_Single_Url.format(''))

        pattern_uuid = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        pattern_url = '^{0}{1}$'.format(url, pattern_uuid)

        match_url_to_job = re.fullmatch(pattern_url, url_to_job)
        assert isinstance(match_url_to_job, re.Match)
        assert match_url_to_job[0] == url_to_job

        match_job_id = re.search(pattern_uuid, url_to_job)
        assert isinstance(match_job_id, re.Match)

        job_id = match_job_id[0]
        exists_job1 = await db_session.get(Job, job_id)
        assert isinstance(exists_job1, Job)


        # clear db
        await db_session.delete(exists_job1)
        await db_session.commit()

