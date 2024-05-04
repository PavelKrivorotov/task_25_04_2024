from fastapi import Depends
from fastapi import Path
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.validators import Re_UUID

from job.models import Job


async def current_job(
    job_id: str = Path(pattern=Re_UUID),
    db: AsyncSession = Depends(get_async_session)
) -> Job:
    
    job = await db.get(Job, job_id)
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The job item `{}` is not found'.format(job_id)
        )
    
    return job

