import uuid
import datetime

from app.utils import get_external_url_to_route
from job import urls as job_urls
from employee.schemas import ReadUserEmployee


class TestReadUserEmployee:
    read_user_employee = ReadUserEmployee(
        id=uuid.UUID('4325491f-15b9-44a6-b4b1-0e6047d3decb'),
        username='my-user-username',
        first_name='MyName',
        last_name='MySurname',
        date_of_employment=datetime.date(year=2024, month=5, day=2),
        is_superuser=False,
        is_staff=True
    )

    def test_model_dump(self):
        assert self.read_user_employee.model_dump() == {
            'user': {
                'id': '4325491f-15b9-44a6-b4b1-0e6047d3decb',
                'username': 'my-user-username',
                'first_name': 'MyName',
                'last_name': 'MySurname',
                'date_of_employment': '2024-05-02',
                'is_superuser': False,
                'is_staff': True
            },
            'job': get_external_url_to_route(job_urls.Me_Url)
        }

