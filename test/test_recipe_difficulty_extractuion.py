# -*- coding: utf-8 -*-
from unittest import TestCase

from recipe_difficulty_extractuion import EASY
from recipe_difficulty_extractuion import HARD
from recipe_difficulty_extractuion import is_recipe_difficult
from recipe_difficulty_extractuion import time_in_minutes
from recipe_difficulty_extractuion import UNDEFINED


class TestIsRecipeDifficult(TestCase):
    def test_all_time_less_than_15__easy(self):
        time_array = ['PT9M', 'PT12M']
        response = is_recipe_difficult(time_array)
        self.assertEqual(EASY, response)

    def test_all_time_greater_than_30__easy(self):
        time_array = ['PT32M', 'PT1H2M']
        response = is_recipe_difficult(time_array)
        self.assertEqual(HARD, response)

    def test_mix_time(self):
        time_array = ['PT29M', 'PT1H2M']
        response = is_recipe_difficult(time_array)
        self.assertEqual(HARD, response)

    def test_unexpected_format(self):
        time_array = ['PT', '12M']
        response = is_recipe_difficult(time_array)
        self.assertEqual(UNDEFINED, response)


class TestTimeInMinutes(TestCase):
    def setUp(self):
        pass

    def test_empty_string(self):
        time_string = ''
        time = time_in_minutes(time_string)
        self.assertEqual(time, 0)

    def test_no_hour_string(self):
        time_string = 'PT54M'
        time = time_in_minutes(time_string)
        self.assertEqual(time, 54)

    def test_no_minute_string(self):
        time_string = 'PT5HS'
        time = time_in_minutes(time_string)
        self.assertEqual(time, 300)

    def test_all_zero(self):
        time_string = '0000'
        time = time_in_minutes(time_string)
        self.assertEqual(time, 0)

    def test_unexpected_format(self):
        time_string = '1MPT'
        time = time_in_minutes(time_string)
        self.assertEqual(time, 0)
