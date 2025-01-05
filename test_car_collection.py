import unittest
from unittest import mock
from io import StringIO
from car_collection import Car, CarCollection

class TestCarCollection(unittest.TestCase):
    def setUp(self):
        """Set up a CarCollection instance for testing."""
        self.manager = CarCollection()
        self.manager.cars = [
            Car("Toyota", "2020", "Corolla"),
            Car("Honda", "2018", "Civic"),
            Car("Ford", "2021", "Focus")
        ]

    def test_add_car(self):
        """Test adding a car to the collection."""
        self.manager.add_car("Mazda", "2022", "CX-5")
        self.assertEqual(len(self.manager.cars), 4)
        self.assertEqual(self.manager.cars[-1].brand, "Mazda")

    def test_modify_car(self):
        """Test modifying an existing car."""
        self.manager.modify_car(1, brand="Nissan", year="2019")
        self.assertEqual(self.manager.cars[1].brand, "Nissan")
        self.assertEqual(self.manager.cars[1].year, "2019")

    def test_modify_car_invalid_index(self):
        """Test modifying a car with an invalid index."""
        with mock.patch('sys.stdout', new=StringIO()) as buf:
            self.manager.modify_car(10, brand="Tesla")
            output = buf.getvalue().strip()
            self.assertEqual(output, "Invalid index. No car modified.")

    def test_display_cars(self):
        """Test displaying all cars."""
        expected_output = (
            "1. Toyota - 2020 - Corolla\n"
            "2. Honda - 2018 - Civic\n"
            "3. Ford - 2021 - Focus"
        )
        with mock.patch('sys.stdout', new=StringIO()) as buf:
            self.manager.display_cars()
            output = buf.getvalue().strip()
            self.assertEqual(output, expected_output)

    def test_display_cars_empty(self):
        """Test displaying cars when the collection is empty."""
        self.manager.cars = []
        with mock.patch('sys.stdout', new=StringIO()) as buf:
            self.manager.display_cars()
            output = buf.getvalue().strip()
            self.assertEqual(output, "No cars in the collection.")

    def test_save_to_csv(self):
        """Test saving cars to a CSV file."""
        with mock.patch("builtins.open", mock.mock_open()) as mocked_file:
            self.manager.save_to_csv("test.csv")
            mocked_file.assert_called_once_with("test.csv", mode='w', newline='')

    def test_load_from_csv(self):
        """Test loading cars from a CSV file."""
        mock_data = "Chevrolet,2022,Impala\nMazda,2020,CX-30\n"
        with mock.patch("builtins.open", mock.mock_open(read_data=mock_data)):
            self.manager.load_from_csv("test.csv")
            self.assertEqual(len(self.manager.cars), 2)
            self.assertEqual(self.manager.cars[0].brand, "Chevrolet")

    def test_load_from_csv_file_not_found(self):
        """Test loading from a CSV file that doesn't exist."""
        with mock.patch('sys.stdout', new=StringIO()) as buf:
            self.manager.load_from_csv("nonexistent.csv")
            output = buf.getvalue().strip()
            self.assertEqual(output, "File nonexistent.csv not found. Starting with an empty collection.")
            self.assertEqual(len(self.manager.cars), 0)

    def test_visualize_data_bar_graph(self):
        """Test visualizing data as an ASCII bar graph."""
        with mock.patch("builtins.input", return_value="1"), mock.patch("sys.stdout", new=StringIO()) as buf:
            self.manager.visualize_data()
            output = buf.getvalue()
            self.assertIn("Toyota", output)
            self.assertIn("Honda", output)
            self.assertIn("Ford", output)

    def test_visualize_data_pivot_table(self):
        """Test visualizing data as a pivot table."""
        with mock.patch("builtins.input", return_value="2"), mock.patch("sys.stdout", new=StringIO()) as buf:
            self.manager.visualize_data()
            output = buf.getvalue()
            self.assertIn("Pivot Table", output)
            self.assertIn("Toyota", output)
            self.assertIn("Honda", output)
            self.assertIn("Ford", output)

    def test_visualize_data_invalid_choice(self):
        """Test visualizing data with an invalid choice."""
        with mock.patch("builtins.input", return_value="3"), mock.patch("sys.stdout", new=StringIO()) as buf:
            self.manager.visualize_data()
            output = buf.getvalue().strip()
            expected_output = (
                "Choose a visualization method:\n"
                "1. ASCII Bar Graph\n"
                "2. Pivot Table\n"
                "Invalid choice. Returning to the menu."
            )
            self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()

