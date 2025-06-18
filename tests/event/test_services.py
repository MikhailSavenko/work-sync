from django.test import TestCase
from rest_framework import serializers

from tests.factories import UserFactory, MeetingFactory
from event.services.meeting import validate_workers_and_include_creator, is_datetime_available

import datetime


class MeetingServiceTestCase(TestCase):

    DATETIME_NOW = datetime.datetime.now(datetime.timezone.utc)

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

        cls.meeting0 = MeetingFactory(creator=cls.worker0, datetime=cls.DATETIME_NOW)
        cls.meeting0.workers.set(cls.two_workers)
    
    def test_validate_workers_and_include_creator_not_workers(self):
        with self.assertRaises(serializers.ValidationError):
            validate_workers_and_include_creator(creator=self.worker0, workers=self.empty_workers)
    
    def test_validate_workers_and_include_creator_workers_qe_2(self):
        with self.assertRaises(serializers.ValidationError):
            validate_workers_and_include_creator(creator=self.worker0, workers=self.one_workers)
        
    def test_validate_workers_and_include_creator_not_in_workers(self):
        result = validate_workers_and_include_creator(creator=self.worker0, workers=self.two_workers)
        
        self.assertEqual(result, self.two_workers + [self.worker0])
    
    def test_is_datetime_available_true_meeting_none(self):
        result = is_datetime_available(worker=self.worker0, check_date=self.DATETIME_NOW)

        self.assertEqual(result, True)
    
    def test_is_datetime_available_false_meeting_none(self):
        result = is_datetime_available(worker=self.worker1, check_date=self.DATETIME_NOW)

        self.assertEqual(result, False)

    def test_is_datetime_available_true_meeting_not_none(self):
        result = is_datetime_available(worker=self.worker0, check_date=self.DATETIME_NOW)

        self.assertEqual(result, True)

