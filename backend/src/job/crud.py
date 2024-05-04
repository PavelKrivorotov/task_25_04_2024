from typing import Optional, Any

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User

from job.models import Job, UserJob
from job.schemas import (
    ReadJob,
    PrivacyReadJob,
    ListJob,
    PrivacyListJob
)


class JobCRUD:
    async def me(
        self,
        db: AsyncSession,
        user: User
    ) -> dict[str, Any]:
        
        query = (
            select(Job)
            .join_from(Job, UserJob, Job.id == UserJob.job_id)
            .where(UserJob.user_id == user.id)
        )
        job = await db.scalar(query)

        return PrivacyReadJob(
            id=job.id,
            title=job.title,
            salary=job.salary,
            days_to_promotion=job.days_to_promotion,
            user_id=user.id
        ).model_dump()

    async def retrieve(
        self,
        job: Job,
        user: Optional[User] = None
    ) -> dict[str, Any]:
        
        if user is None or user.is_staff:
            model = ReadJob
        else:
            model = PrivacyReadJob
        
        return model.model_validate(job).model_dump()

    async def list(
        self,
        db: AsyncSession,
        user: Optional[User] = None
    ) -> list[Any]:

        result = await db.scalars(select(Job).order_by(Job.id))
        count = await db.scalar(func.count(Job.id))

        data = {}
        data['count'] = count

        if user is None or user.is_staff:
            model = ListJob
        else:
            model = PrivacyListJob

        data['results'] = model(data=result.all()).model_dump()
        return data

job_crud = JobCRUD()

