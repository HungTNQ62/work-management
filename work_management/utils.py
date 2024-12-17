import os
import configparser
import jwt

from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework import generics

from .settings import EMAIL_HOST_USER,SIMPLE_JWT
from .responses import ResponseObject, ErrorResponse
from users.models import User


class Email(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        recipient_list = request.data.get('recipient_list')
        message = request.data.get('message')
        subject = request.data.get('subject')
        if not recipient_list or not message or not subject:
            return JsonResponse(ErrorResponse(errors="Missing recipient list or message or subject").to_dict())

        send_Email(recipient_list, EMAIL_HOST_USER, message, subject)
        return JsonResponse(ResponseObject(message="Send email successfully").to_dict())


def send_Email(recipient_list: list, from_email = None, message = None, subject = None):
    if not isinstance(recipient_list, list):
        recipient_list = [recipient_list]
    return send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list,
        fail_silently = False
    ) 

def get_user_from_request(request):
    token = request.headers.get('Authorization')
    user_id = jwt.decode(token, SIMPLE_JWT.get('SIGNING_KEY'), algorithms=["HS256"]).get('user_id')
    user = User.objects.get(id=user_id)
    return user