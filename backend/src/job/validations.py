import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from job.models import Job


async def validate_job_exists(
    db: AsyncSession,
    job_id: uuid.UUID
) -> bool:
    
    query = (
        select(
            select(Job.id)
            .where(Job.id == job_id)
            .exists()
        )
    )
    exists = await db.scalar(query)
    return exists

