import uuid
import datetime

from app.utils import get_external_url_to_route

from admin.job.schemas import CreateJob, RepresentJob
from admin.job.urls import Job_Single_Url


class TestCreateJob:
    create_job_1 = CreateJob(
        title='Intern python developer',
        salary=20000,
        days_to_promotion=180
    )

    def test_to_dict(self):
        assert self.create_job_1.to_dict() == {
            'title': 'Intern python developer',
            'salary': 20000,
            'days_to_promotion': datetime.timedelta(days=180)
        }


class TestRepresentJob:
    represent_job_1 = RepresentJob(
        id=uuid.UUID('bc6c457f-4712-4832-8d8a-c0935d6607bc')
    )

    def test_model_dump(self):
        path = Job_Single_Url.format('bc6c457f-4712-4832-8d8a-c0935d6607bc')
        assert self.represent_job_1.model_dump() == {
            'job': get_external_url_to_route(path)
        }

