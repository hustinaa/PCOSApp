from django.contrib import admin
from django.urls import path
from pcosapp import views
from .views import login_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # Default view is the login page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('index/', views.index_view, name='index'),  # Form page
    path('recommend_meals/', views.get_meal_plan, name='recommend_meals'),  # Recommendation page
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("settings/", views.settings_view, name="settings"),
    path("delete-account/", views.delete_account, name="delete_account"),
    path('meal-plan/saved/', views.saved_meal_plan, name='saved_meal_plan'),
]
