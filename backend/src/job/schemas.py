import datetime
import uuid
from decimal import Decimal
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer

from app.utils import get_external_url_to_route
from employee.urls import Me_Url


class ReadJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str

    user_id: Optional[uuid.UUID] = None

    @model_serializer
    def serializer(self) -> dict[str, Any]:
        data = {}
        
        if self.user_id:
            data['user'] = get_external_url_to_route(Me_Url)

        job = {
            'id': str(self.id),
            'title': self.title,
        }
        data['job'] = job
        return data


class PrivacyReadJob(ReadJob):
    salary: Decimal
    days_to_promotion: datetime.timedelta

    @model_serializer
    def serializer(self) -> dict[str, Any]:
        data = super().serializer()

        job = data['job']
        job['salary'] = float(self.salary)
        job['days_to_promotion'] = self.days_to_promotion.days
        return data


class ListJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[ReadJob]

    @model_serializer
    def serializer(self) -> list[Any]:
        return [item.model_dump()['job'] for item in self.data]


class PrivacyListJob(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    data: list[PrivacyReadJob]

    @model_serializer
    def serializer(self) -> list[Any]:
        return [item.model_dump()['job'] for item in self.data]

