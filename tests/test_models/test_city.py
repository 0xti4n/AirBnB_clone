#!/usr/bin/python3
"""Test City"""
import unittest
import pep8
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.review import Review


class Testcity(unittest.TestCase):

    def test_pep8_conformance_city(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/city.py'])
        self.assertEqual(result.total_errors, 0, "\
Found code style errors (and warnings).")

    def test_class(self):
        """ test """
        city1 = City()
        self.assertEqual(city1.__class__.__name__, "City")

    def test_father(self):
        """ Test """
        city1 = City()
        self.assertTrue(issubclass(city1.__class__, BaseModel))
