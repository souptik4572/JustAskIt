from django.db import models
from ..question.models import Question
from ..user.models import EndUser
from ..constants.vote_type_constants import VOTE_TYPES, UP_VOTE

# Create your models here.


class Answer(models.Model):
    answer = models.CharField(max_length=10000)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    owner = models.ForeignKey(EndUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} for question {self.question.id}"


class AnswerVote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    voter = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    vote_type = models.CharField(
        max_length=5, choices=VOTE_TYPES, default=UP_VOTE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} for answer {self.answer.id}"
