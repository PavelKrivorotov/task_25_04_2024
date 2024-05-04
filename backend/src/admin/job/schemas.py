import uuid
import datetime
from typing import Annotated, Any

from fastapi import Form
from pydantic import BaseModel, model_serializer

from app.utils import get_external_url_to_route
from admin.job.urls import Job_Single_Url


class CreateJob:
    def __init__(
        self,
        title: Annotated[
            str,
            Form(min_length=1, max_length=150)
        ],
        salary: Annotated[
            float,
            Form(ge=0, le=1000000)
        ],
        days_to_promotion: Annotated[
            int,
            Form(ge=1, le=1000)
        ]
    ) -> None:
        
        self.title = title
        self.salary = salary
        self.days_to_promotion = days_to_promotion

    def to_dict(self) -> dict[str, Any]:
        data = {}
        data['title'] = self.title
        data['salary'] = self.salary
        data['days_to_promotion'] = datetime.timedelta(days=self.days_to_promotion)
        return data


class RepresentJob(BaseModel):
    id: uuid.UUID

    @model_serializer
    def serializer(self) -> dict[str, Any]:
        path = Job_Single_Url.format(self.id)
        return {
            'job': get_external_url_to_route(path)
        }

