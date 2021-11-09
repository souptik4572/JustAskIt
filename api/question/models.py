from django.db import models
from ..user.models import EndUser
from ..constants.ask_type_constants import ASK_TYPES, PUBLIC

# Create your models here.


class Question(models.Model):
    question = models.CharField(max_length=500)
    ask_type = models.CharField(
        max_length=7, choices=ASK_TYPES, default=PUBLIC)
    owner = models.ForeignKey(EndUser, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.question}"
