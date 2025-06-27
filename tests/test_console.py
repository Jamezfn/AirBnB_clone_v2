import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.state import State
from models.place import Place
import os

class TestHBNBCommandCreate(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.console = HBNBCommand()
        storage._FileStorage__objects = {}

    def tearDown(self):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_create_no_class(self):
        """Test create command with no class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

    def test_create_invalid_class(self):
        """Test create command with invalid class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create InvalidClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_create_state_with_params(self):
        """Test create State with parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd('create State name="California"')
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            obj = storage.all()[f"State.{obj_id}"]
            self.assertEqual(obj.name, "California")

    def test_create_place_with_params(self):
        """Test create Place with multiple parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = ('create Place city_id="0001" user_id="0001" '
                   'name="My_little_house" number_rooms=4 number_bathrooms=2 '
                   'max_guest=10 price_by_night=300 latitude=37.773972 '
                   'longitude=-122.431297')
            self.console.onecmd(cmd)
            obj_id = f.getvalue().strip()
            self.assertTrue(len(obj_id) > 0)
            obj = storage.all()[f"Place.{obj_id}"]
            self.assertEqual(obj.city_id, "0001")
            self.assertEqual(obj.user_id, "0001")
            self.assertEqual(obj.name, "My little house")
            self.assertEqual(obj.number_rooms, 4)
            self.assertEqual(obj.number_bathrooms, 2)
            self.assertEqual(obj.max_guest, 10)
            self.assertEqual(obj.price_by_night, 300)
            self.assertEqual(obj.latitude, 37.773972)
            self.assertEqual(obj.longitude, -122.431297)

    def test_create_with_invalid_params(self):
        """Test create with invalid parameters"""
        with patch('sys.stdout', new=StringIO()) as f:
            cmd = 'create State name="California" invalid_param=abc number=42.5'
            self.console.onecmd(cmd)
            obj_id = f.getvalue().strip()
            obj = storage.all()[f"State.{obj_id}"]
            self.assertEqual(obj.name, "California")
            self.assertEqual(obj.number, 42.5)
            self.assertFalse(hasattr(obj, "invalid_param"))

if __name__ == '__main__':
    unittest.main()
