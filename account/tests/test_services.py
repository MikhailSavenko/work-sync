from django.test import TestCase

from account.tests.factories import TeamFactory, UserFactory
from account.services.team import get_worker_with_team, is_your_team


class TeamServiceTestCase(TestCase):
    TWO_STR = "2"

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
    
    def test_is_your_team_is_none(self):
        result = is_your_team(team_pk=self.TWO_STR, worker=self.worker1)
        
        self.assertEqual(result, False)

    def test_is_your_team(self):
        result = is_your_team(team_pk=self.team0.id, worker=self.worker0)
    
        self.assertEqual(result, True)