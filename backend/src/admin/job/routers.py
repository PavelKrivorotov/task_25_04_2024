from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session

from auth.depends import is_admin
from auth.models import User

from job.depends import current_job
from job.models import Job
from job.crud import job_crud

from admin.job.schemas import CreateJob
from admin.job.crud import admin_job_crud


router = APIRouter()


@router.post('/create', dependencies=[Depends(is_admin)])
async def create_job(
    data: Annotated[CreateJob, Depends()],
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    job = await admin_job_crud.create(db, data)
    return JSONResponse(
        content=job,
        status_code=status.HTTP_201_CREATED
    )


@router.get('/jobs/all')
async def list_jobs(
    user: User = Depends(is_admin),
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    jobs = await job_crud.list(db, user)
    return JSONResponse(content=jobs)


@router.get('/jobs/{job_id}')
async def retrieve_job(
    job: Job = Depends(current_job),
    user: User = Depends(is_admin),
) -> JSONResponse:
    
    job = await job_crud.retrieve(job, user)
    return JSONResponse(content=job)

