from datetime import datetime, time

from django.test import TestCase
from django.utils import timezone

from account.utils import get_day_bounds, get_month_bounds


class GetDayBoundsTestCase(TestCase):

    START_DATE_WITH_DAY = "2025-05-01"
    END_DATE_WITH_DAY = "2025-05-10"

    @classmethod
    def setUpTestData(cls):
        cls.start_date = datetime.strptime(cls.START_DATE_WITH_DAY, "%Y-%m-%d").date()
        cls.end_date = datetime.strptime(cls.END_DATE_WITH_DAY, "%Y-%m-%d").date()

    def test_value_error_if_tuple_not_equal_2(self):
        tuple_three_items = (self.start_date, self.start_date, self.start_date)
        with self.assertRaises(ValueError):
            get_day_bounds(tuple_three_items)

    def test_value_error_if_tuple_empty(self):
        tuple_empty = ()
        with self.assertRaises(ValueError):
            get_day_bounds(tuple_empty)

    def test_value_not_datetime_type(self):
        tuple_not_datetime = (self.START_DATE_WITH_DAY, self.END_DATE_WITH_DAY)
        with self.assertRaises(TypeError):
            get_day_bounds(tuple_not_datetime)

    def test_valid_range_date_input(self):
        tuple_valid_range = (self.start_date, self.end_date)

        start_dt, end_db = get_day_bounds(date=tuple_valid_range)
        self.assertIsInstance(start_dt, datetime)
        self.assertIsInstance(end_db, datetime)
        self.assertTrue(timezone.is_aware(start_dt))
        self.assertTrue(timezone.is_aware(end_db))
        self.assertEqual(start_dt.date(), self.start_date)
        self.assertEqual(end_db.date(), self.end_date)
        self.assertEqual(start_dt.time(), time.min)
        self.assertEqual(end_db.time(), time.max)

    def test_valid_single_date_input(self):
        start_dt, end_db = get_day_bounds(date=self.start_date)

        self.assertIsInstance(start_dt, datetime)
        self.assertIsInstance(end_db, datetime)
        self.assertTrue(timezone.is_aware(start_dt))
        self.assertTrue(timezone.is_aware(end_db))
        self.assertEqual(start_dt.date(), self.start_date)
        self.assertEqual(end_db.date(), self.start_date)
        self.assertEqual(start_dt.time(), time.min)
        self.assertEqual(end_db.time(), time.max)


class GetMonthBoundsTestCase(TestCase):

    LAST_MAY_DAY = 31
    DATE_MONTH = "2025-05"

    @classmethod
    def setUpTestData(cls):
        cls.parse_date = datetime.strptime(cls.DATE_MONTH, "%Y-%m").date()

    def test_type_error_if_not_datetime(self):
        with self.assertRaises(TypeError):
            get_day_bounds(date=self.DATE_MONTH)

    def test_valid_value_input(self):
        start_dt, end_dt = get_month_bounds(start_date=self.parse_date)

        end_end_date = self.parse_date.replace(day=self.LAST_MAY_DAY)
        self.assertIsInstance(start_dt, datetime)
        self.assertIsInstance(end_dt, datetime)
        self.assertTrue(timezone.is_aware(start_dt))
        self.assertTrue(timezone.is_aware(end_dt))
        self.assertEqual(start_dt.date(), self.parse_date)
        self.assertEqual(end_dt.date(), end_end_date)
        self.assertEqual(start_dt.time(), time.min)
        self.assertEqual(end_dt.time(), time.max)
