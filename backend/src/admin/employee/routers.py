from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.validators import Re_UUID

from auth.depends import is_admin
from auth.models import User

from admin.employee.crud import admin_employee_crud


router = APIRouter()


@router.get('/employees/all', dependencies=[Depends(is_admin)])
async def list_employees(
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    employees = await admin_employee_crud.list(db)
    return JSONResponse(content=employees)


@router.get('/employees/{user_id}')
async def retrieve_employees(
    user_id: str = Path(pattern=Re_UUID),
    user: User = Depends(is_admin),
    db: AsyncSession = Depends(get_async_session)
) -> JSONResponse:
    
    if user_id == str(user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Information about `Admin` is not allowed'
        )

    employee = await admin_employee_crud.retrieve(db, user_id)
    return JSONResponse(content=employee)

