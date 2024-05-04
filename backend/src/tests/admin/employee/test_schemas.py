import uuid
import datetime

from admin.employee.schemas import ReadEmployee, ListEmployee


class TestReadEmployee:
    read_employee1 = ReadEmployee(
        user_id=uuid.UUID('1ffa53ac-7c89-4492-9781-44574156af06'),
        username='MyUserName',
        first_name='MyFirstName',
        last_name='MyLastName',
        date_of_employment=datetime.date(year=2024, month=5, day=2),
        is_superuser=False,
        is_staff=True,
        job_id=uuid.UUID('271b1ab1-e1cd-4c55-a3a7-80247f3e68e6'),
        title='Intern python developer',
        salary=20000,
        days_to_promotion=datetime.timedelta(days=180)
    )

    def test_model_dump(self):
        assert self.read_employee1.model_dump() == {
            'user': {
                'id': '1ffa53ac-7c89-4492-9781-44574156af06',
                'username': 'MyUserName',
                'first_name': 'MyFirstName',
                'last_name': 'MyLastName',
                'date_of_employment': '2024-05-02',
                'is_superuser': False,
                'is_staff': True,
            },
            'job': {
                'id': '271b1ab1-e1cd-4c55-a3a7-80247f3e68e6',
                'title': 'Intern python developer',
                'salary': 20000,
                'days_to_promotion': 180
            }
        }


class TestListEmployee:
    list_employees = ListEmployee(
        data=[
            ReadEmployee(
                user_id=uuid.UUID('1ffa53ac-7c89-4492-9781-44574156af06'),
                username='MyUserName1',
                first_name='MyFirstName1',
                last_name='MyLastName1',
                date_of_employment=datetime.date(year=2024, month=5, day=2),
                is_superuser=False,
                is_staff=True,
                job_id=uuid.UUID('271b1ab1-e1cd-4c55-a3a7-80247f3e68e6'),
                title='Intern python developer',
                salary=20000,
                days_to_promotion=datetime.timedelta(days=180)
            ),
            ReadEmployee(
                user_id=uuid.UUID('2bc0baaa-caa8-475c-8a65-3f5f061b9480'),
                username='MyUserName2',
                first_name='MyFirstName2',
                last_name='MyLastName2',
                date_of_employment=datetime.date(year=2024, month=5, day=2),
                is_superuser=False,
                is_staff=True,
                job_id=uuid.UUID('26d72932-54d4-4588-8c2f-4b18f1f24f57'),
                title='Junior python developer',
                salary=50000,
                days_to_promotion=datetime.timedelta(days=365)
            ),
            ReadEmployee(
                user_id=uuid.UUID('01cee843-a106-4ed8-85ca-92c93588db44'),
                username='MyUserName3',
                first_name='MyFirstName3',
                last_name='MyLastName3',
                date_of_employment=datetime.date(year=2024, month=5, day=2),
                is_superuser=False,
                is_staff=True,
                job_id=uuid.UUID('33547205-b6de-46c0-a2bd-0d7dae917652'),
                title='Middle python developer',
                salary=100000,
                days_to_promotion=datetime.timedelta(days=540)
            )
        ]
    )

    def test_model_dump(self):
        assert self.list_employees.model_dump() == [
            {
                'user': {
                    'id': '1ffa53ac-7c89-4492-9781-44574156af06',
                    'username': 'MyUserName1',
                    'first_name': 'MyFirstName1',
                    'last_name': 'MyLastName1',
                    'date_of_employment': '2024-05-02',
                    'is_superuser': False,
                    'is_staff': True,
                },
                'job': {
                    'id': '271b1ab1-e1cd-4c55-a3a7-80247f3e68e6',
                    'title': 'Intern python developer',
                    'salary': 20000,
                    'days_to_promotion': 180
                }
            },
            {
                'user': {
                    'id': '2bc0baaa-caa8-475c-8a65-3f5f061b9480',
                    'username': 'MyUserName2',
                    'first_name': 'MyFirstName2',
                    'last_name': 'MyLastName2',
                    'date_of_employment': '2024-05-02',
                    'is_superuser': False,
                    'is_staff': True,
                },
                'job': {
                    'id': '26d72932-54d4-4588-8c2f-4b18f1f24f57',
                    'title': 'Junior python developer',
                    'salary': 50000,
                    'days_to_promotion': 365
                }
            },
            {
                'user': {
                    'id': '01cee843-a106-4ed8-85ca-92c93588db44',
                    'username': 'MyUserName3',
                    'first_name': 'MyFirstName3',
                    'last_name': 'MyLastName3',
                    'date_of_employment': '2024-05-02',
                    'is_superuser': False,
                    'is_staff': True,
                },
                'job': {
                    'id': '33547205-b6de-46c0-a2bd-0d7dae917652',
                    'title': 'Middle python developer',
                    'salary': 100000,
                    'days_to_promotion': 540
                }
            },
        ]

