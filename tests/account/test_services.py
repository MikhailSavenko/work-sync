from django.test import TestCase
import datetime
from tests.factories import TeamFactory, UserFactory, TaskDeadlineFactory, MeetingFactory, EvaluationFactory
from account.services.team import get_worker_with_team, is_your_team
from account.services.worker import format_calendar_text_table, get_calendar_events, get_evaluations_avg


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


class WorkerServiceTestCase(TestCase):
    
    DATE_NO_IVENTS_START = datetime.datetime(2024, 12, 31, 23, 59, 59, tzinfo=datetime.timezone.utc)
    DATE_NO_IVENTS_END = datetime.datetime(2025, 1, 1, 23, 59, 59, tzinfo=datetime.timezone.utc)
    DATETIME_NOW = datetime.datetime.now(datetime.timezone.utc)
    TIMEDELTA_THREE_DAYS = datetime.timedelta(days=3)
    
    TABLE_VALUE_WITOUT_DATA = 215
    TABLE_VALUE_WITH_TWO_TASK = 440
    TABLE_VALUE_WITOUT_DATA_IN_LIST = 4

    ZERO = 0
    ONE = 1
    TWO = 2

    FLOAT_FIVE = 5.0

    @classmethod
    def setUpTestData(cls):
        cls.user0 = UserFactory()
        cls.user1 = UserFactory()

        cls.worker0 = cls.user0.worker
        cls.worker1 = cls.user1.worker

        cls.empty_meetings = []
        cls.empty_tasks = []

        cls.task0 = TaskDeadlineFactory(deadline=cls.DATE_NO_IVENTS_START)
        cls.task1 = TaskDeadlineFactory(deadline=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))

        cls.meeting0 = MeetingFactory(creator=cls.worker0, datetime=(cls.DATETIME_NOW + cls.TIMEDELTA_THREE_DAYS))
        cls.meeting0.workers.set([cls.worker0])

        cls.task0.executor = cls.worker0
        cls.task0.save()
        cls.task1.executor = cls.worker0
        cls.task1.save()

        cls.task_list = [cls.task0, cls.task1]

        cls.evaluation = EvaluationFactory(to_worker=cls.worker0, task=cls.task1)

    def test_format_calendar_text_table_empty_input(self):
        result = format_calendar_text_table(meetings=self.empty_meetings, tasks=self.empty_tasks)

        self.assertEqual(self.TABLE_VALUE_WITOUT_DATA, len(result))
        self.assertEqual(str, type(result))
    
    def test_format_calendar_text_table_valid_input(self):
        result = format_calendar_text_table(meetings=self.empty_meetings, tasks=self.task_list)

        self.assertEqual(self.TABLE_VALUE_WITH_TWO_TASK, len(result))
        self.assertEqual(str, type(result))

    def test_get_calendar_events_input_worker_without_events(self):
        result = get_calendar_events(worker=self.worker1, start_date=self.DATE_NO_IVENTS_START, end_date=self.DATE_NO_IVENTS_END)
        
        self.assertEqual(result["meetings"].count(), self.ZERO)
        self.assertEqual(result["tasks"].count(), self.ZERO)
        self.assertEqual(len(result["table"]), self.TABLE_VALUE_WITOUT_DATA_IN_LIST)

    def test_get_calendar_events_input_worker_with_events(self):
        result = get_calendar_events(worker=self.worker0, start_date=(self.DATETIME_NOW - self.TIMEDELTA_THREE_DAYS), end_date=(self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS + self.TIMEDELTA_THREE_DAYS))
        
        self.assertEqual(result["meetings"].count(), self.ONE)
        self.assertEqual(result["tasks"].count(), self.ONE)

    def test_get_evaluations_avg_no_evaluation(self):
        result = get_evaluations_avg(worker=self.worker1, start=self.DATE_NO_IVENTS_START, end=self.DATE_NO_IVENTS_END)

        self.assertEqual(result["average_score"], None)
        self.assertEqual(result["evaluations_count"], self.ZERO)
    
    def test_get_evaluations_avg_with_evaluation(self):
        result = get_evaluations_avg(worker=self.worker0, start=(self.DATETIME_NOW - self.TIMEDELTA_THREE_DAYS), end=(self.DATETIME_NOW + self.TIMEDELTA_THREE_DAYS))

        self.assertEqual(result["average_score"], self.FLOAT_FIVE)
        self.assertEqual(result["evaluations_count"], self.ONE)
