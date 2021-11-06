from django.urls import path
from .views.user import register_end_user, login_user, get_user_profile, edit_user_profile, request_password_reset, update_password
from .views.location import add_new_location, edit_existing_location, delete_existing_location
from .views.education import add_new_education, edit_existing_education, delete_existing_education

urlpatterns = [
    # All User routes. All routes concern User data and User Model
    path('register/', register_end_user, name='api.register_end_user'),
    path('login/', login_user, name='api.login_user'),
    path('profile/', get_user_profile, name='api.get_user_profile'),
    path('edit-profile/', edit_user_profile, name='api.edit_user_profile'),
    path('request-password-reset/', request_password_reset,
         name='api.request_password_reset'),
    path('update-password/', update_password,
         name='api.update_password'),

    # All Location routes for a particular user
    path('location/new/', add_new_location, name='api.add_new_location'),
    path('location/<int:location_id>/edit/',
         edit_existing_location, name='api.edit_existing_location'),
    path('location/<int:location_id>/delete/',
         delete_existing_location, name='api.delete_existing_location'),

    # All Education routes for a particular user
    path('education/new/', add_new_education, name='api.add_new_education'),
    path('education/<int:education_id>/edit/',
         edit_existing_education, name='api.edit_existing_education'),
    path('education/<int:education_id>/delete/',
         delete_existing_education, name='api.delete_existing_education')
]
