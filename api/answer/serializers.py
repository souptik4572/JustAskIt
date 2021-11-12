from rest_framework import serializers
from .models import Answer
from ..question.serializers import QuestionSerializer


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'created_at', 'updated_at')
