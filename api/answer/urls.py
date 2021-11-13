from django.urls import path
from .views import create_new_answer, edit_existing_answer, delete_existing_answer, get_all_answers, get_answer_to_particular_question

urlpatterns = [
    path('all/', get_all_answers, name='api.get_all_answers'),
    path('question/<int:question_id>/', get_answer_to_particular_question,
         name='api.get_answer_to_particular_question'),
    path('new/to-question/<int:question_id>/',
         create_new_answer, name='api.create_new_answer'),
    path('<int:answer_id>/edit/', edit_existing_answer,
         name='api.edit_existing_answer'),
    path('<int:answer_id>/delete/', delete_existing_answer,
         name='api.delete_existing_answer'),
]
