#!/usr/bin/python3
"""Test Place"""
import unittest
import pep8
from models.user import User
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.review import Review


class Testplace(unittest.TestCase):
    def test_pep8_conformance_place(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/place.py'])
        self.assertEqual(result.total_errors, 0, "\
Found code style errors (and warnings).")

    def test_class(self):
        """ Test """
        place1 = Place()
        self.assertEqual(place1.__class__.__name__, "Place")

    def test_father(self):
        """ Test """
        place1 = Place()
        self.assertTrue(issubclass(place1.__class__, BaseModel))

    def test_place(self):
        """
        Test attributes of Class Place
        """
        my_amenity = Amenity()
        my_city = City()
        my_user = User()
        my_place = Place()
        my_place.city_id = my_city.id
        my_place.user_id = my_user.id
        my_place.name = 'Coworking'
        my_place.description = 'description'
        my_place.number_rooms = 4
        my_place.number_bathrooms = 2
        my_place.max_guest = 4
        my_place.price_by_night = 200
        my_place.latitude = 25.0342808
        my_place.longitude = -77.3962784
        my_place.amenity_ids = str(my_amenity.id)
        self.assertEqual(my_place.city_id, my_city.id)
        self.assertEqual(my_place.user_id, my_user.id)
        self.assertEqual(my_place.name, 'Coworking')
        self.assertEqual(my_place.description, 'description')
        self.assertEqual(my_place.number_rooms, 4)
        self.assertTrue(type(my_place.number_rooms), int)
        self.assertEqual(my_place.number_bathrooms, 2)
        self.assertTrue(type(my_place.number_bathrooms), int)
        self.assertEqual(my_place.max_guest, 4)
        self.assertTrue(type(my_place.max_guest), int)
        self.assertEqual(my_place.price_by_night, 200)
        self.assertTrue(type(my_place.price_by_night), int)
        self.assertEqual(my_place.latitude, 25.0342808)
        self.assertTrue(type(my_place.latitude), float)
        self.assertEqual(my_place.longitude, -77.3962784)
        self.assertTrue(type(my_place.longitude), float)
        self.assertEqual(my_place.amenity_ids, str(my_amenity.id))
        self.assertTrue(type(my_place.amenity_ids), str)
