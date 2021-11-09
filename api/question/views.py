from django.http import JsonResponse
from django.utils.decorators import decorator_from_middleware, decorator_from_middleware_with_args
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import QuestionSerializer
from .models import Question
from django.views.decorators.csrf import csrf_exempt
import json
from ..constants.ask_type_constants import LIMITED, PUBLIC
from ..middleware.auth_strategy import AuthStrategyMiddleware

# Create your views here.


@csrf_exempt
@api_view(['GET'])
def get_all_questions(request):
    try:
        questions = Question.objects.filter(ask_type=PUBLIC).all()
        return JsonResponse({
            'success': True,
            'message': 'All questions from the portal',
            'questions': QuestionSerializer(questions, many=True).data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PUT'])
@decorator_from_middleware(AuthStrategyMiddleware)
def create_new_question(request):
    data = json.loads(request.body)
    try:
        question = data['question']
        endUser = request.user
        new_question = Question.objects.create(
            question=question, owner=endUser)
        return JsonResponse({
            'success': True,
            'message': 'Successfully created question',
            'question': QuestionSerializer(new_question).data
        }, status=status.HTTP_201_CREATED)
    except KeyError:
        return JsonResponse({
            'success': False,
            'message': 'Question body parameter not found'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['PATCH'])
@decorator_from_middleware(AuthStrategyMiddleware)
def edit_existing_question(request, question_id):
    data = json.loads(request.body)
    try:
        existing_question = Question.objects.get(
            id=question_id, owner__id=request.user.id)
        if 'question' in data:
            existing_question.question = data['question']
        existing_question.save()
        return JsonResponse({
            'success': True,
            'message': 'Successfully updated question',
            'question': QuestionSerializer(existing_question).data
        }, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Question does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['DELETE'])
@decorator_from_middleware(AuthStrategyMiddleware)
def delete_existing_question(request, question_id):
    try:
        existing_question = Question.objects.get(
            id=question_id, owner__id=request.user.id)
        existing_question.delete()
        return JsonResponse({
            'success': True,
            'message': 'Successfully deleted question',
        }, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Question does not exist'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_404_NOT_FOUND)