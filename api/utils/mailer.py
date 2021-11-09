from django.http import JsonResponse
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config
from rest_framework import status

sendgrid_key = config("SENDGRID_API_KEY")
PASSWORD_RESET_EMAIL_TEMPLATE_ID = config('PASSWORD_RESET_EMAIL_TEMPLATE_ID')
FROM_EMAIL = config('FROM_EMAIL')


def send_password_reset_email(data):
    reset_password_link = f"justaskit.com/password-reset?token={data['token']}&id={data['id']}"
    message = Mail(from_email=FROM_EMAIL, to_emails=[data['receiver']])
    message.dynamic_template_data = {
        'reset_password_link': reset_password_link
    }
    message.template_id = PASSWORD_RESET_EMAIL_TEMPLATE_ID
    try:
        sendgrid = SendGridAPIClient(api_key=sendgrid_key)
        sendgrid.send(message)
    except Exception as e:
        JsonResponse({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
