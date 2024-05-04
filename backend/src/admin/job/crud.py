from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from job.models import Job
from admin.job.schemas import CreateJob, RepresentJob


class AdminJobCRUD:
    async def create(
        self,
        db: AsyncSession,
        data: CreateJob
    ) -> dict[str, Any]:
        
        job = Job(**data.to_dict())
        db.add(job)
        await db.commit()
        await db.refresh(job)
        return RepresentJob(id=job.id).model_dump()

admin_job_crud = AdminJobCRUD()

