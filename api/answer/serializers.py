from rest_framework import serializers
from .models import Answer


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'answer', 'created_at', 'updated_at')
