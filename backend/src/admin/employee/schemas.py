import uuid
import datetime
from typing import Any
from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer


class ReadEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    date_of_employment: datetime.date
    is_superuser: bool
    is_staff: bool

    job_id: uuid.UUID
    title: str
    salary: Decimal
    days_to_promotion: datetime.timedelta

    @model_serializer
    def serializer(self) -> dict[str, Any]:
        return {
            'user': {
                'id': str(self.user_id),
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'date_of_employment': self.date_of_employment.strftime('%Y-%m-%d'),
                'is_superuser': self.is_superuser,
                'is_staff': self.is_staff,
            },
            'job': {
                'id': str(self.job_id),
                'title': self.title,
                'salary': float(self.salary),
                'days_to_promotion': self.days_to_promotion.days
            }
        }


class ListEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[ReadEmployee]

    @model_serializer
    def derializer(self) -> list[ReadEmployee]:
        return self.data

