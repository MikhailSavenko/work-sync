from django.test import TestCase
from rest_framework import serializers

from account.tests.factories import UserFactory
from event.services.meeting import validate_workers_and_include_creator


class MeetingServiceTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user0 = UserFactory()
        cls.user1 = UserFactory()
        cls.user2 = UserFactory()

        cls.worker0 = cls.user0.worker
        cls.worker1 = cls.user1.worker
        cls.worker2 = cls.user2.worker

        cls.two_workers = [cls.worker1, cls.worker2]
        cls.one_workers = [cls.worker0]
        cls.empty_workers = []
    
    def test_validate_workers_and_include_creator_not_workers(self):
        with self.assertRaises(serializers.ValidationError):
            validate_workers_and_include_creator(creator=self.worker0, workers=self.empty_workers)
    
    def test_validate_workers_and_include_creator_workers_qe_2(self):
        with self.assertRaises(serializers.ValidationError):
            validate_workers_and_include_creator(creator=self.worker0, workers=self.one_workers)
        
    def test_validate_workers_and_include_creator_not_in_workers(self):
        result = validate_workers_and_include_creator(creator=self.worker0, workers=self.two_workers)
        
        self.assertEqual(result, self.two_workers + [self.worker0])