import uuid
from typing import Annotated, Any

from fastapi import Form
from pydantic import BaseModel, model_serializer

from app.validators import Re_UUID
from app.utils import get_external_url_to_route

from employee.urls import Me_Url as Employee_Me_Url
from job.urls import Me_Url as Job_Me_Url


class CreateUser:
    def __init__(
        self,
        username: Annotated[
            str,
            Form(min_length=1, max_length=128)
        ],
        password: Annotated[
            str,
            Form(min_length=1, max_length=128)
        ],
        first_name: Annotated[
            str,
            Form(min_length=1, max_length=150)
        ],
        last_name: Annotated[
            str,
            Form(min_length=1, max_length=150)
        ],
        job_id: Annotated[
            str,
            Form(pattern=Re_UUID)
        ]
    ) -> None:

        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.job_id = uuid.UUID(job_id)

    def to_dict(self) -> dict[str, Any]:
        return {
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name' : self.last_name,
        }


class RepresentUser(BaseModel):
    @model_serializer
    def serializer(self) -> dict[str, Any]:
        return {
            'user': get_external_url_to_route(Employee_Me_Url),
            'job': get_external_url_to_route(Job_Me_Url)
        }

