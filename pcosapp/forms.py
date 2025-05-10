from django import forms

# Activity level choices
ACTIVITY_CHOICES = [
    ('sedentary', 'Sedentary (Not Active)'),
    ('lightly_active', 'Lightly Active'),
    ('moderately_active', 'Moderately Active'),
    ('very_active', 'Very Active'),
    ('super_active', 'Super Active'),
]

class UserInputForm(forms.Form):
    # Weight input in kilograms
    weight = forms.FloatField(
        label="Weight (kg)",
        min_value=0,
        help_text="Enter your weight in kilograms.",
    )
    
    # Height input in centimeters
    height = forms.FloatField(
        label="Height (cm)",
        min_value=0,
        help_text="Enter your height in centimeters.",
    )
    
    # Age input
    age = forms.IntegerField(
        label="Age (years)",
        min_value=0,
        help_text="Enter your age in years.",
    )
    
    # Activity level choice as dropdown
    activity_level = forms.ChoiceField(
        label="Activity Level",
        choices=ACTIVITY_CHOICES,
    )
    
    # Dietary restrictions with checkboxes
    restrictions = forms.MultipleChoiceField(
        label="Dietary Restrictions",
        required=False,
        choices=[
            ('nuts', 'Nuts'),
            ('red meat', 'Red Meat'),
            ('seafood', 'Seafood'),
        ],
        widget=forms.CheckboxSelectMultiple,
        help_text="Select any dietary restrictions you have (optional).",
    )