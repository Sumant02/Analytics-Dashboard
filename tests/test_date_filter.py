import unittest
from datetime import date, datetime, time

from fastapi import HTTPException

from main import build_filter


class BuildDateFilterTests(unittest.TestCase):
    def test_includes_both_selected_days(self):
        query = build_filter(
            customer_name=None,
            category=None,
            product=None,
            min_amount=None,
            max_amount=None,
            start_date=date(2025, 1, 10),
            end_date=date(2025, 1, 12),
        )

        self.assertEqual(
            query['order_date'],
            {
                '$gte': datetime.combine(date(2025, 1, 10), time.min),
                '$lte': datetime.combine(date(2025, 1, 12), time.max),
            },
        )

    def test_supports_a_single_sided_range(self):
        query = build_filter(
            customer_name=None,
            category=None,
            product=None,
            min_amount=None,
            max_amount=None,
            start_date=None,
            end_date=date(2025, 1, 12),
        )

        self.assertEqual(
            query['order_date'],
            {'$lte': datetime.combine(date(2025, 1, 12), time.max)},
        )

    def test_rejects_start_date_after_end_date(self):
        with self.assertRaises(HTTPException) as error:
            build_filter(
                customer_name=None,
                category=None,
                product=None,
                min_amount=None,
                max_amount=None,
                start_date=date(2025, 1, 13),
                end_date=date(2025, 1, 12),
            )

        self.assertEqual(error.exception.status_code, 422)
