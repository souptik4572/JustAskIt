from rest_framework import serializers
from .models import Answer, AnswerVote
from ..question.serializers import QuestionSerializer


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'answer', 'created_at', 'updated_at')


class AnswerVoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnswerVote
        fields = ('id', 'vote_type', 'created_at', 'updated_at')
