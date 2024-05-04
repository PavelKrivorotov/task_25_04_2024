from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session

from auth.depends import is_staff
from auth.models import User

from job.depends import current_job
from job.crud import job_crud
from job.models import Job


router = APIRouter()


@router.get('/me')
async def my_job(
    user: User = Depends(is_staff),
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    job = await job_crud.me(db, user)
    return JSONResponse(content=job)


@router.get('/jobs/all')
async def list_jobs(
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    jobs = await job_crud.list(db)
    return JSONResponse(content=jobs)


@router.get('/jobs/{job_id}')
async def retrieve_job(
    job: Job = Depends(current_job),
) -> JSONResponse:
    
    job = await job_crud.retrieve(job)
    return JSONResponse(content=job)

