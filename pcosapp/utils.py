from pcosapp.models import Recipe
import random

def generate_recipe_dict():
    recipe_dict = {}
    
    # Fetch all recipes from the database
    recipes = Recipe.objects.all()

    for recipe in recipes:
        # Creating the dictionary for each recipe using the specified format
        recipe_dict[recipe.recipe_id] = {
            1: recipe.meal_name,
            2: recipe.protein_content,
            3: recipe.ingredients,
            4: recipe.keywords,
            5: recipe.recipe_category
        }
    
    return recipe_dict


def normalize_category(recipes):
    """ Normalize recipes into categories (Breakfast, Lunch, Dinner) based on their category at index 5. """
    categorized_recipes = {
        'breakfast': [],
        'lunch': [],
        'dinner': []
    }

    for recipe in recipes:
        # Access the category at index 5
        category = recipe.get(5)  # Assuming index 5 is where the category is stored
        normalized_category = None
        
        # Check if category is not None and normalize it
        if category and isinstance(category, str):
            if 'breakfast' in category.lower():
                normalized_category = 'breakfast'
            elif 'dinner' in category.lower():
                normalized_category = 'dinner'
            else:
                normalized_category = 'lunch'

        # If a valid category is found, add the recipe to the respective list
        if normalized_category:
            categorized_recipes[normalized_category].append(recipe)

    # Print summary of categorized recipes
    print(f"Available for Breakfast: {len(categorized_recipes['breakfast'])}")
    print(f"Available for Lunch: {len(categorized_recipes['lunch'])}")
    print(f"Available for Dinner: {len(categorized_recipes['dinner'])}")
    print('----------------------------------------------')
    print('')
    
    return categorized_recipes


def knapsack_algorithm(categorized_recipes, protein_min, protein_max):
    protein_min = float(protein_min)
    protein_max = float(protein_max)

    breakfast_cap = protein_max * 0.4
    lunch_cap = protein_max * 0.3

    selected_recipes = {'breakfast': [], 'lunch': [], 'dinner': []}
    total_protein = 0.0

    # Helper function to select the best recipe under a protein cap
    def select_best_recipe(recipes, cap):
        best_recipe = None
        best_protein = 0.0

        for recipe in recipes:
            protein = float(recipe[2])  # Assuming protein content is at index 2
            if protein > best_protein and protein <= cap:
                best_recipe = recipe
                best_protein = protein

        return best_recipe

    # Select the best breakfast recipe under the breakfast cap
    best_breakfast = select_best_recipe(categorized_recipes['breakfast'], breakfast_cap)
    if best_breakfast:
        selected_recipes['breakfast'].append(best_breakfast)
        breakfast_protein = float(best_breakfast[2])
        total_protein += breakfast_protein
        categorized_recipes['breakfast'].remove(best_breakfast)  # Remove selected recipe
    else:
        breakfast_protein = 0.0  # No recipe selected

    # Select the best lunch recipe under the lunch cap
    best_lunch = select_best_recipe(categorized_recipes['lunch'], lunch_cap)
    if best_lunch:
        selected_recipes['lunch'].append(best_lunch)
        lunch_protein = float(best_lunch[2])
        total_protein += lunch_protein
        categorized_recipes['lunch'].remove(best_lunch)  # Remove selected recipe
    else:
        lunch_protein = 0.0  # No recipe selected

    # Calculate the dinner cap based on remaining protein after breakfast and lunch
    dinner_cap = protein_max - (breakfast_protein + lunch_protein)

    # Select the best dinner recipe under the dinner cap
    best_dinner = select_best_recipe(categorized_recipes['dinner'], dinner_cap)
    if best_dinner:
        selected_recipes['dinner'].append(best_dinner)
        total_protein += float(best_dinner[2])
        categorized_recipes['dinner'].remove(best_dinner)  # Remove selected recipe

    # Verify that the total protein meets the minimum requirement
    if total_protein < protein_min:
        print(f"Total protein {total_protein:.2f} is less than the minimum required {protein_min:.2f}.")
        return None

    print(f"Selected Recipes: {selected_recipes}")
    print(f"Total Protein: {total_protein:.2f}")

    return selected_recipes
