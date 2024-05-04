import datetime
import uuid

from app.utils import get_external_url_to_route
from job.schemas import ReadJob, PrivacyReadJob, ListJob, PrivacyListJob
from employee import urls as employee_urls


class TestReadJob:
    read_job_1 = ReadJob(
        id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
        title='Intern python developer'
    )

    read_job_2 = ReadJob(
        id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
        title='Intern python developer',
        user_id=uuid.UUID('9c321671-a331-4055-a051-b796b74fe119')
    )

    def test_model_dump(self):
        assert self.read_job_1.model_dump() == {
            'job': {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer'
            }
        }

        assert self.read_job_2.model_dump() == {
            'user': get_external_url_to_route(employee_urls.Me_Url),
            'job': {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer'
            }
        }


class TestPrivacyReadJob:
    read_job_privacy_1 = PrivacyReadJob(
        id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
        title='Intern python developer',
        salary=20000,
        days_to_promotion=datetime.timedelta(days=180)
    )

    read_job_privacy_2 = PrivacyReadJob(
        id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
        title='Intern python developer',
        salary=20000,
        days_to_promotion=datetime.timedelta(days=180),
        user_id=uuid.UUID('9c321671-a331-4055-a051-b796b74fe119')
    )

    def test_model_dump(self):
        assert self.read_job_privacy_1.model_dump() == {
            'job': {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            }
        }

        assert self.read_job_privacy_2.model_dump() == {
            'user': get_external_url_to_route(employee_urls.Me_Url),
            'job': {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            }
        }


class TestListJob:
    list_jobs = ListJob(
        data = [
            ReadJob(
                id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
                title='Intern python developer',
            ),
            ReadJob(
                id=uuid.UUID('0d4c7a4c-0890-4a91-8a3d-a9c288679e5c'),
                title='Junior python developer',
            ),
            ReadJob(
                id=uuid.UUID('4fab266a-8a4c-4fa5-a101-cc194a00103b'),
                title='Middle python developer',
            ),
        ]
    )

    def test_model_dump(self):
        assert self.list_jobs.model_dump() == [
            {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer',
            },
            {
                'id': '0d4c7a4c-0890-4a91-8a3d-a9c288679e5c',
                'title': 'Junior python developer',
            },
            {
                'id': '4fab266a-8a4c-4fa5-a101-cc194a00103b',
                'title': 'Middle python developer',
            },
        ]


class TestPrivacyListJob:
    list_jobs = PrivacyListJob(
        data = [
            PrivacyReadJob(
                id=uuid.UUID('087a4b94-3316-4790-8be8-88b85546d948'),
                title='Intern python developer',
                salary=20000,
                days_to_promotion=datetime.timedelta(days=180)
            ),
            PrivacyReadJob(
                id=uuid.UUID('0d4c7a4c-0890-4a91-8a3d-a9c288679e5c'),
                title='Junior python developer',
                salary=50000,
                days_to_promotion=datetime.timedelta(days=365)
            ),
            PrivacyReadJob(
                id=uuid.UUID('4fab266a-8a4c-4fa5-a101-cc194a00103b'),
                title='Middle python developer',
                salary=100000,
                days_to_promotion=datetime.timedelta(days=540)
            ),
        ]
    )

    def test_model_dump(self):
        assert self.list_jobs.model_dump() == [
            {
                'id': '087a4b94-3316-4790-8be8-88b85546d948',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            },
            {
                'id': '0d4c7a4c-0890-4a91-8a3d-a9c288679e5c',
                'title': 'Junior python developer',
                'salary': 50000,
                'days_to_promotion': 365
            },
            {
                'id': '4fab266a-8a4c-4fa5-a101-cc194a00103b',
                'title': 'Middle python developer',
                'salary': 100000,
                'days_to_promotion': 540
            }
        ]

