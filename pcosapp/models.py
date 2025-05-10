from django.db import models
from django.contrib.auth.models import User

class SavedMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_plan = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Meal Plan ({self.created_at.strftime('%Y-%m-%d %H:%M:%S')})"

class Recipe(models.Model):
    # Unique identifier for the recipe
    recipe_id = models.IntegerField(primary_key=True)

    # Basic recipe details
    meal_name = models.CharField(max_length=255)

    # Nutritional information
    protein_content = models.FloatField(null=True, blank=True)  # Allow missing protein content

    # Ingredients (stored as JSON for flexibility)
    ingredients = models.JSONField(null=True, blank=True)  # JSON for ingredients, as they may have a complex structure

    # Keywords for search or filtering (now a simple CharField)
    keywords = models.CharField(max_length=1024, null=True, blank=True)  # Now a plain string (comma-separated)

    # Recipe categorization
    recipe_category = models.CharField(max_length=255)

    def __str__(self):
        return self.meal_name