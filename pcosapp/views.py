from django.shortcuts import render, redirect
from .forms import UserInputForm
from .utils import generate_recipe_dict, normalize_category, knapsack_algorithm  # Updated to import generate_recipe_dict
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import SavedMealPlan


@login_required
def settings_view(request):
    return render(request, "settings.html", {"username": request.user.username})

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Log the user out
        user.delete()  # Delete the user's account
        return redirect("login")  # Redirect to the login page

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {'show_sidebar': False})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully!")
            return redirect('login')
    return render(request, 'signup.html', {'show_sidebar': False})

def index_view(request):
    username = request.user.username if request.user.is_authenticated else 'Guest'
    return render(request, 'index.html', {'form': UserInputForm(), 'username': username, 'show_sidebar': True})

def calculate_bmi(weight, height):
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)

    # Determine BMI category
    if bmi < 18.5:
        description = "Underweight"
    elif 18.5 <= bmi <= 24.9:
        description = "Normal weight"
    elif 25 <= bmi <= 29.9:
        description = "Overweight"
    elif 30 <= bmi <= 34.9:
        description = "Obesity Class 1"
    else:
        description = "Obesity Class 2 or higher"

    print(f"BMI calculated: {bmi} ({description})")
    return bmi, description


def calculate_bmr(weight, height, age):
    bmr = 10 * weight + 6.25 * height - 5 * age - 161
    print(f"BMR calculated: {bmr}")
    return bmr

def calculate_tdee(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    print(f"TDEE calculated: {tdee}")
    return tdee

def calculate_protein_intake(tdee):
    protein_min = tdee * 0.15 / 4  # 1g of protein = 4 kcal
    protein_max = tdee * 0.2 / 4  # 1g of protein = 4 kcal
    print(f"Protein range: {protein_min}g to {protein_max}g")
    print('----------------------------------------------')
    return protein_min, protein_max


def filter_recipes_by_restrictions(recipes, restrictions):
    print('')
    print(f"Number of recipes before filtering: {len(recipes)}")
    print(f"Filtering recipes with restrictions: {restrictions}")
    filtered_recipes = []
    
    # Define meat-related keywords to look for
    meat_keywords = ['meat', 'bacon', 'beef', 'pork', 'sausage', 'dogs', 'ham']
    seafood_keywords = ['fish', 'shrimp', 'squid', 'tuna']
    nuts_keywords = ['nuts', 'peanut', 'oyster']

    for recipe_id, recipe in recipes.items():
        # Get the ingredients from the recipe, assumed to be at index 3
        ingredients = recipe.get(3, '')
        
        # Check restrictions
        for restriction in restrictions:
            restriction = restriction.lower()  # Ensure case-insensitivity
            
            if restriction == "red meat":
                # If any meat-related keyword is found in ingredients, skip this recipe
                if any(keyword in ingredients for keyword in meat_keywords):
                    break  # Skip this recipe
            elif restriction == "seafood":
                # If any meat-related keyword is found in ingredients, skip this recipe
                if any(keyword in ingredients for keyword in seafood_keywords):
                    break  # Skip this recipe
            else:
                # Check if the restriction is found in other aspects like keywords or ingredients
                if any(keyword in ingredients for keyword in nuts_keywords):
                    break  # Skip this recipe
        else:
            # If no restrictions matched, include the recipe
            filtered_recipes.append(recipe)

    print(f"Number of recipes after filtering: {len(filtered_recipes)}")
    print('----------------------------------------------')
    print('')
    return filtered_recipes

def get_meal_plan(request):
    if request.method == "POST":
        print("Received POST request for meal plan generation.")

        # Step 1: Get user data from the form
        weight = float(request.POST.get('weight', 0))
        height = float(request.POST.get('height', 0))
        age = int(request.POST.get('age', 0))
        activity_level = request.POST.get('activity_level', 'sedentary')
        restrictions = request.POST.getlist('restrictions')
        print(f"User inputs - Weight: {weight}, Height: {height}, Age: {age}, Activity Level: {activity_level}, Restrictions: {restrictions}")

        # Step 2: Calculate BMI, BMR, TDEE, and protein intake
        bmi, bmi_description = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity_level)
        protein_min, protein_max = calculate_protein_intake(tdee)

        # Step 3: Fetch and filter recipes
        recipe_dict = generate_recipe_dict()
        filtered_recipes = filter_recipes_by_restrictions(recipe_dict, restrictions) if restrictions else list(recipe_dict.values())
        categorized_recipes = normalize_category(filtered_recipes)

        # Step 4: Generate a weekly meal plan
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        week_plan = []

        # Generate meal plan for each day
        for i in range(7):
            daily_plan = knapsack_algorithm(categorized_recipes, protein_min, protein_max)
            
            # Ensure daily_plan is not None before proceeding
            if daily_plan:
                week_plan.append({
                    'day': days_of_week[i],
                    'breakfast': [{
                        'name': recipe[1],
                        'protein': recipe[2],
                        'ingredients': recipe[3]
                    } for recipe in daily_plan['breakfast']],
                    'lunch': [{
                        'name': recipe[1],
                        'protein': recipe[2],
                        'ingredients': recipe[3]
                    } for recipe in daily_plan['lunch']],
                    'dinner': [{
                        'name': recipe[1],
                        'protein': recipe[2],
                        'ingredients': recipe[3]
                    } for recipe in daily_plan['dinner']],
                })


            print("Meal Recommendation plan ready!")
        

        # Step 5: Save the plan in the database
        if request.user.is_authenticated:
            SavedMealPlan.objects.update_or_create(
                user=request.user,
                defaults={'meal_plan': {
                    'bmi': bmi,
                    'bmi_description': bmi_description, 
                    'bmr': bmr,
                    'protein_min': protein_min,
                    'protein_max': protein_max,
                    'week_plan': week_plan
                }}
            )
        # Step 6: Render the meal plan to the recommendations.html
        return render(request, 'recommendations.html', {
            'week_plan': week_plan,
            'bmi': bmi,
            'bmi_description': bmi_description,
            'bmr': bmr,
            'protein_min': protein_min,
            'protein_max': protein_max,
            'show_sidebar': True
        })
    
    print("Received GET request to display input form.")
    return render(request, 'index.html', {'form': UserInputForm()})

def settings_view(request):
    username = request.user.username if request.user.is_authenticated else 'Guest'
    return render(request, 'settings.html', {'username': username, 'show_sidebar': True})

def saved_meal_plan(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        saved_plan = SavedMealPlan.objects.get(user=request.user)
        meal_plan = saved_plan.meal_plan
    except SavedMealPlan.DoesNotExist:
        return render(request, 'saved_plan.html', {'message': 'No saved meal plan found.', 'show_sidebar': True})

    return render(request, 'saved_plan.html', {
        'bmi': meal_plan['bmi'],
        'bmi_description': meal_plan['bmi_description'],
        'bmr': meal_plan['bmr'],
        'protein_min': meal_plan['protein_min'],
        'protein_max': meal_plan['protein_max'],
        'week_plan': meal_plan['week_plan'],
        'show_sidebar': True
    })
