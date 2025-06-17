from django.test import TestCase

from account.tests.factories import TeamFactory, UserFactory
from account.services.team import get_worker_with_team


class TeamServiceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user0 = UserFactory()
        cls.user1 = UserFactory()

        cls.worker0 = cls.user0.worker
        cls.worker1 = cls.user1.worker
        
        cls.team0 = TeamFactory()

        cls.worker0.team = cls.team0
        cls.worker0.team.save()

        cls.two_workers = [cls.worker0, cls.worker1]

    def test_get_worker_with_team(self):
        result = get_worker_with_team(workers=self.two_workers)

        self.assertEqual(1, len(result))
        self.assertEqual(result[0], self.worker0)