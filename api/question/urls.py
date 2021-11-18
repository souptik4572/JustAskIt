from django.urls import path

from .views import (create_new_question, delete_existing_question,
                    edit_existing_question, get_all_questions,
                    get_all_questions_of_logged_user)

urlpatterns = [
    path('', get_all_questions_of_logged_user,
         name='api.get_all_questions_of_logged_user'),
    path('all/', get_all_questions, name='api.get_all_questions'),
    path('new/', create_new_question, name='api.create_new_question'),
    path('<int:question_id>/edit/', edit_existing_question,
         name='api.edit_existing_question'),
    path('<int:question_id>/delete/', delete_existing_question,
         name='api.delete_existing_question')
]
