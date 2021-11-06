from django.http import JsonResponse

# Create your views here.
def home():
    return JsonResponse({
        'success': True,
        'message': "Welcome, This is the home page."
    })