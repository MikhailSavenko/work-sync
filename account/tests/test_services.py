from django.test import TestCase

from account.models import Worker, Team, User


class TeamServiceTestCase(TestCase):
    EMAIL_CREATOR = "test_email@gmail.com"
    PASSWORD = "superpassword123/"

    @classmethod
    def setUpTestData(cls):
        cls.user_creator = User.objects.create_user(email=cls.EMAIL_CREATOR, password=cls.PASSWORD)
        cls.worker_creator = cls.user_creator.worker
        
        cls.team = Team.objects.create()
        cls.workers = Worker.objects.bulk_create()