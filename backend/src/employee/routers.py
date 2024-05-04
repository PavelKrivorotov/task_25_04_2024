from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse

from auth.depends import is_staff
from auth.models import User
from employee.schemas import ReadUserEmployee


router = APIRouter()


@router.get('/me')
async def me(
    user: User = Depends(is_staff),
) -> JSONResponse:

    employee = ReadUserEmployee.model_validate(user).model_dump()
    return JSONResponse(content=employee)

