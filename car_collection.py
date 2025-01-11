import csv
import pandas as pd


class Car:
    def __init__(self, brand, year, model):
        self.brand = brand
        self.year = year
        self.model = model

    def __str__(self):
        return f"{self.brand} - {self.year} - {self.model}"


class CarCollection:
    filename = 'data.csv'

    def __init__(self):
        self.cars = []

    def load_from_csv(self, filename):
        """Loads cars from a CSV file."""
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                self.cars = [Car(*row) for row in reader]
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty collection.")
            self.cars = []  # Clear the collection when the file is not found

    def save_to_csv(self, filename):
        """Saves cars to a CSV file."""
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for car in self.cars:
                writer.writerow([car.brand, car.year, car.model])

    def display_cars(self):
        """Displays all cars in the collection."""
        if not self.cars:
            print("No cars in the collection.")
            return
        for i, car in enumerate(self.cars, start=1):
            print(f"{i}. {car}")

    def add_car(self, brand, year, model):
        """Adds a new car to the collection."""
        new_car = Car(brand, year, model)
        self.cars.append(new_car)

    def modify_car(self, index, brand=None, year=None, model=None):
        """Modifies an existing car in the collection."""
        if 0 <= index < len(self.cars):
            car = self.cars[index]
            if brand:
                car.brand = brand
            if year:
                # Optionally check if the year is valid (if needed, you can convert to int)
                try:
                    car.year = str(int(year))  # Ensure year is a string (or raise ValueError)
                except ValueError:
                    print(f"Invalid year format: {year}. No changes made.")
                    return
            if model:
                car.model = model
        else:
            print("Invalid index. No car modified.")

    def visualize_data(self):
        """Visualizes the data as an ASCII bar graph or pivot table."""
        if not self.cars:
            print("No cars in the collection to visualize.")
            return

        print("\nChoose a visualization method:")
        print("1. ASCII Bar Graph (Car Count by Manufacturer)")
        print("2. ASCII Bar Graph (Car Count by Model Type)")
        print("3. ASCII Bar Graph (Car Count by Year)")
        print("4. Pivot Table (Car Count by Manufacturer and Model Type)")
        print("5. Pivot Table (Car Count by Manufacturer and Year)")  # New option
        choice = input("Enter your choice: ")

        # Convert cars to a DataFrame for pandas operations
        data = [{'Brand': car.brand, 'Year': car.year, 'Model': car.model} for car in self.cars]
        df = pd.DataFrame(data)

        if choice == '1':
            # Count cars by brand
            brand_counts = df['Brand'].value_counts()

            # Display ASCII bar graph
            print("\nCar Count by Manufacturer:")
            max_width = 50  # Maximum width of the bar in characters
            max_count = brand_counts.max() if not brand_counts.empty else 1

            for brand, count in brand_counts.items():
                bar_length = int((count / max_count) * max_width)
                print(f"{brand:15}: {'#' * bar_length} ({count})")

        elif choice == '2':
            # Count cars by model type (e.g., Sedan, SUV)
            model_counts = df['Model'].value_counts()

            # Display ASCII bar graph for each model type
            print("\nCar Count by Model Type:")
            max_width = 50  # Maximum width of the bar in characters
            max_count = model_counts.max() if not model_counts.empty else 1

            for model, count in model_counts.items():
                bar_length = int((count / max_count) * max_width)
                print(f"{model:15}: {'#' * bar_length} ({count})")

        elif choice == '3':
            # Count cars by year
            year_counts = df['Year'].value_counts().sort_index()

            # Display ASCII bar graph for each year
            print("\nCar Count by Year:")
            max_width = 50  # Maximum width of the bar in characters
            max_count = year_counts.max() if not year_counts.empty else 1

            for year, count in year_counts.items():
                bar_length = int((count / max_count) * max_width)
                print(f"{year:4}: {'#' * bar_length} ({count})")

        elif choice == '4':
            # Ensure all model types are displayed (even those with zero counts)
            all_models = df['Model'].unique()

            # Create a pivot table for Car Count by Manufacturer and Model Type
            pivot = df.pivot_table(index='Brand', columns='Model', aggfunc='size', fill_value=0)

            # Add a 'Car Count' column showing the total number of cars per brand
            pivot['Car Count'] = pivot.sum(axis=1)

            # Ensure that all model types appear in the pivot table (even if some have zero counts)
            pivot = pivot[["Car Count"] + list(all_models)]  # Reorder columns to have 'Car Count' first

            # Add a "Total" row that sums up the counts across all brands
            pivot.loc['Total'] = pivot.sum(axis=0)

            # Show the pivot table
            print("\nPivot Table (Car Count and Vehicle Type Counts by Manufacturer):")

            # Set pandas options to display full table without truncation
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)  # Disable line wrapping for the table
            print(pivot)

        elif choice == '5':  # New pivot table option
            # Create a pivot table for Car Count by Manufacturer and Year
            pivot = df.pivot_table(index='Brand', columns='Year', aggfunc='size', fill_value=0)

            # Add a 'Car Count' column showing the total number of cars per brand
            pivot['Car Count'] = pivot.sum(axis=1)

            # Ensure that all years are displayed (even if some have zero counts)
            all_years = sorted(df['Year'].unique())

            # Reorder columns to have 'Car Count' first
            pivot = pivot[["Car Count"] + list(all_years)]

            # Add a "Total" row that sums up the counts across all manufacturers
            pivot.loc['Total'] = pivot.sum(axis=0)

            # Show the pivot table
            print("\nPivot Table (Car Count by Manufacturer and Year):")

            # Set pandas options to display full table without truncation
            pd.set_option('display.max_columns', None)  # Show all columns
            pd.set_option('display.width', None)  # Disable line wrapping for the table
            print(pivot)

        else:
            print("Invalid choice. Returning to the menu.")


def main():
    # Create an instance of the CarCollection class
    manager = CarCollection()

    # Load the car data from the 'data.csv' file into the CarCollection instance
    manager.load_from_csv('data.csv')

    # Infinite loop to keep the program running until the user chooses to exit
    while True:
        # Display the menu options to the user
        print("\nCar Collection Manager")
        print("1. Display cars")
        print("2. Add car")
        print("3. Modify car")
        print("4. Visualize data")
        print("5. Save and exit")

        # Get the user's choice for the menu option
        choice = input("Enter your choice: ")

        # Option 1: Display all cars in the collection
        if choice == '1':
            manager.display_cars()

        # Option 2: Add a new car to the collection
        elif choice == '2':
            # Prompt the user for the car details (brand, year, and model)
            brand = input("Enter car brand: ")
            year = input("Enter car year: ")
            model = input("Enter car model: ")
            # Add the new car to the collection using the provided details
            manager.add_car(brand, year, model)

        # Option 3: Modify an existing car's details
        elif choice == '3':
            # Display the list of cars to let the user select which one to modify
            manager.display_cars()
            try:
                # Ask the user to input the number of the car to modify (convert to index)
                index = int(input("Enter the number of the car to modify: ")) - 1
                # Prompt the user for new details, allowing blank input to keep existing values
                brand = input("Enter new brand (or leave blank): ")
                year = input("Enter new year (or leave blank): ")
                model = input("Enter new model (or leave blank): ")
                # Modify the selected car's details
                manager.modify_car(index, brand or str, year or int, model or str)
            except ValueError:
                # Handle invalid input for selecting the car to modify
                print("Invalid input. Please enter a valid number.")

        # Option 4: Visualize the data (e.g., display an ASCII bar graph or pivot table)
        elif choice == '4':
            manager.visualize_data()

        # Option 5: Save changes to the CSV file and exit the program
        elif choice == '5':
            # Save the car collection to the 'data.csv' file
            manager.save_to_csv('data.csv')
            # Inform the user that changes have been saved and exit the loop
            print("Changes saved. Exiting.")
            break

        # If the user inputs an invalid option, inform them and prompt again
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
