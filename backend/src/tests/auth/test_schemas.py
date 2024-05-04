import uuid

from app.utils import get_external_url_to_route
from auth.schemas import CreateUser, RepresentUser

from employee import urls as employee_urls
from job import urls as job_urls


class TestCreateUser:
    create_user = CreateUser(
        username='test-create-user',
        password='ojd73d3d',
        first_name='TestCreateUser',
        last_name='TestCreateUser',
        job_id='e575645e-7a51-49ea-8677-49b943eb93de'
    )

    def test(self):
        assert self.create_user.username == 'test-create-user'
        assert self.create_user.password == 'ojd73d3d'
        assert self.create_user.first_name == 'TestCreateUser'
        assert self.create_user.last_name == 'TestCreateUser'

        assert isinstance(self.create_user.job_id, uuid.UUID)
        assert str(self.create_user.job_id) == 'e575645e-7a51-49ea-8677-49b943eb93de'

    def test_to_dict(self):
        assert self.create_user.to_dict() == {
            'username': 'test-create-user',
            'password': 'ojd73d3d',
            'first_name': 'TestCreateUser',
            'last_name': 'TestCreateUser'
        }


class TestRepresentUser:
    represent = RepresentUser()

    def test_model_dump(self):
        assert self.represent.model_dump() == {
            'user': get_external_url_to_route(employee_urls.Me_Url),
            'job': get_external_url_to_route(job_urls.Me_Url)
        }

