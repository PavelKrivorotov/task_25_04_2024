from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.settings import (
    ALLOW_ORIGINS,
    ALLOW_CREDENTIALS,
    ALLOW_METHODS,
    ALLOW_HEADERS
)

from auth.routers import router as auth_router
from employee.routers import router as employee_router
from job.routers import router as job_router

from admin.job.routers import router as admin_job_router
from admin.employee.routers import router as admin_employee_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS
)

app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(employee_router, prefix='/employee', tags=['Employee'])
app.include_router(job_router, prefix='/job', tags=['Job'])

app.include_router(admin_job_router, prefix='/admin/job', tags=['Admin'])
app.include_router(admin_employee_router, prefix='/admin/employee', tags=['Admin'])

