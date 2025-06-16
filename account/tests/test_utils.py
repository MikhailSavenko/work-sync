from django.test import TestCase
from datetime import datetime, time

from django.utils import timezone


from account.utils import get_day_bounds


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
    


