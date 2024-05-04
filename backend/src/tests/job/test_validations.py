import uuid
import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from job.models import Job
from job.validations import validate_job_exists


@pytest.mark.asyncio(scope='session')
# @pytest.mark.asyncio
async def test_validate_job_exists(db_session: AsyncSession):
    job_1 = {
        'id': uuid.UUID('60f83459-fa9c-4e68-9d4e-bc6c64625659'),
        'title': 'Intern python developer',
        'salary': 20000,
        'days_to_promotion': datetime.timedelta(days=180)
    }

    job1 = Job(**job_1)
    db_session.add(job1)
    await db_session.commit()

    exists_job1 = await validate_job_exists(db_session, job_1['id'])
    assert exists_job1 == True

    exists_job2 = await validate_job_exists(db_session, '11111111-1111-1111-1111-111111111111')
    assert exists_job2 == False


    # cleaer db
    await db_session.delete(job1)
    await db_session.commit()

