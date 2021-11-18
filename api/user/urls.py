from django.urls import path

from .views.education import (add_new_education, delete_existing_education,
                              edit_existing_education)
from .views.employment import (add_new_employment, delete_existing_employment,
                               edit_existing_employment)
from .views.follow import (follow_particular_user, get_all_followees,
                           get_all_followers, unfollow_particular_user)
from .views.location import (add_new_location, delete_existing_location,
                             edit_existing_location)
from .views.user import (edit_user_profile, get_general_user_profile,
                         get_user_profile, login_user, register_end_user,
                         request_password_reset, update_password)

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
    path('<int:user_id>/profile/', get_general_user_profile,
         name='api.get_general_user_profile'),

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
         delete_existing_education, name='api.delete_existing_education'),

    # All Employment routes for a particular user
    path('employment/new/', add_new_employment, name='api.add_new_employment'),
    path('employment/<int:employment_id>/edit/',
         edit_existing_employment, name='api.edit_existing_employment'),
    path('employment/<int:employment_id>/delete/',
         delete_existing_employment, name='api.delete_existing_employment'),

    # All Follow routes for a particular user
    path('<int:user_id>/follow/', follow_particular_user,
         name='api.follow_particular_user'),
    path('<int:user_id>/unfollow/', unfollow_particular_user,
         name='api.unfollow_particular_user'),
    path('followers/', get_all_followers,
         name='api.get_all_followers'),
    path('followees/', get_all_followees,
         name='api.get_all_followees'),
]
