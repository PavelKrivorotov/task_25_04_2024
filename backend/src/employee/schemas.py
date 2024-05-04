import uuid
import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict
from pydantic import model_serializer

from app.utils import get_external_url_to_route
from job.urls import Me_Url


class ReadUserEmployee(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    date_of_employment: datetime.date
    is_superuser: bool
    is_staff: bool

    @model_serializer
    def serializer(self) -> dict[str, Any]:
        user = {}
        user['id'] = str(self.id)
        user['username'] = self.username
        user['first_name'] = self.first_name
        user['last_name'] = self.last_name
        user['date_of_employment'] = self.date_of_employment.strftime('%Y-%m-%d')
        user['is_superuser'] = self.is_superuser
        user['is_staff'] = self.is_staff

        data = {}
        data['user'] = user
        data['job'] = get_external_url_to_route(Me_Url)
        return data

