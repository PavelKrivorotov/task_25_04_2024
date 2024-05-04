from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from job.models import UserJob

from admin.employee.queries import query as q
from admin.employee.converters import convert_employee
from admin.employee.schemas import ReadEmployee, ListEmployee


class AdminEmployeeCRUD:
    async def retrieve(
        self,
        db: AsyncSession,
        user_id: str
    ) -> dict[str, Any]:

        query = q.where(User.id == user_id)
        result = await db.execute(query)

        result_c = convert_employee(result)
        if not result_c:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return ReadEmployee.model_validate(result_c[0]).model_dump()

    async def list(
        self,
        db: AsyncSession,
    ) -> dict[str, Any]:
        
        query = q.order_by(User.id)        
        result = await db.execute(query)
        count = await db.scalar(select(func.count(UserJob.id)))

        result_c = convert_employee(result)
        return {
            'count': count,
            'results': ListEmployee(data=result_c).model_dump()
        }
    
admin_employee_crud = AdminEmployeeCRUD()

