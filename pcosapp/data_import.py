import csv
from pathlib import Path
from pcosapp.models import Recipe
from .utils import normalize_category  # Ensure normalize_category is defined or imported

def load_data():
    dataset_path = Path('pcosapp/dataset.csv')

    # debug debug debug XD
    if not dataset_path.exists():
        print(f"Dataset file not found at {dataset_path}")
        return

    print(f"Loading data from: {dataset_path}")

    # Open the CSV file with UTF-8-SIG encoding
    with open(dataset_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)

        # Normalize headers to remove BOM
        reader.fieldnames = [field.replace('\ufeff', '').strip() for field in reader.fieldnames]
        print(f"Normalized headers: {reader.fieldnames}")

        # Track the number of successfully added recipes
        added_recipes = 0

        # Process each row
        for row in reader:
            # Normalize row keys and values by stripping \ufeff
            normalized_row = {
                key.replace('\ufeff', '').strip(): value.replace('\ufeff', '').strip() if value else value
                for key, value in row.items()
            }
            print(f"Normalized row: {normalized_row}")  # Debugging: Print the normalized row

            # Access Recipe_ID from the normalized row
            recipe_id = normalized_row.get('Recipe_ID')
            if not recipe_id:
                print(f"Skipping row with missing Recipe_ID: {normalized_row}")
                continue

            print(f"Found Recipe_ID: {recipe_id}")  # Debugging: Log valid Recipe_ID

            try:
                # Normalize Recipe_Category
                normalized_category = normalize_category(normalized_row['Recipe_Category'])

                # Clean up the Keywords (comma-separated list of keywords)
                keywords = normalized_row.get('Keywords', '')
                keywords = ', '.join([keyword.strip() for keyword in keywords.split(',')])  # Remove extra spaces and format correctly

                # Create Recipe instance
                recipe = Recipe.objects.create(
                    recipe_id=int(recipe_id),
                    meal_name=normalized_row['Meal_Name'],
                    protein_content=float(normalized_row['Protein_Content']) if normalized_row['Protein_Content'] else None,
                    ingredients=normalized_row.get('Ingredients', None),  # You can keep it as JSON if needed
                    keywords=keywords,  # Now a formatted string
                    recipe_category=normalized_category
                )
                added_recipes += 1
                print(f"Added recipe: {recipe.meal_name}")

            except Exception as e:
                print(f"Failed to add recipe '{normalized_row.get('Meal_Name')}' with error: {e}")

    # Verify total recipes loaded
    print(f"Total recipes loaded: {added_recipes}")