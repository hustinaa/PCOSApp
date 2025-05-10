from django.contrib import admin
from .models import Recipe

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # List view settings
    list_display = ('meal_name', 'protein_content', 'recipe_category')
    list_filter = ('recipe_category',)  # Remove 'keywords' here if it's not suitable
    search_fields = ('meal_name', 'author_name', 'meal_description', 'keywords')
    ordering = ('recipe_id',)

    # Detail view settings
    fieldsets = (
        ("Basic Information", {
            'fields': ('meal_name',)  # Ensure this is a tuple or list
        }),
        ("Nutritional Info", {
            'fields': ('protein_content',)  # Ensure this is a tuple or list
        }),
        ("Ingredients & Instructions", {
            'fields': ('ingredients',)  # Ensure this is a tuple (note the comma)
        }),
        ("Categorization", {
            'fields': ('recipe_category', 'keywords')  # Ensure this is a tuple or list
        }),
    )
    readonly_fields = ('recipe_id',)
