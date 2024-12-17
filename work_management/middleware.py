import jwt

from django.http import JsonResponse

from .responses import ErrorResponse
from .settings import SIMPLE_JWT
from users.models import User
from tasks.models import Tasks

class PermissionMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        response = self.get_response(request)
        return response


    def process_middleware(self, request, view_func, view_args, view_kwargs):
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse(
                    ErrorResponse(errors="Missing authorization header").to_dict()
                )
            
            user_id = jwt.decode(token, SIMPLE_JWT.get('SIGNING_KEY'), algorithms=["HS256"]).get('user_id')
            user = User.objects.get(id=user_id)
            if not user:
                return JsonResponse(
                    ErrorResponse(errors="Not an user").to_dict()
                )
            test_string = "tasks/" + str(view_kwargs.get("id"))
            if (test_string in request.build_absolute_uri()):
                check = False
                task = Tasks.objects.get(id=view_kwargs.get("id"))
                if user_id == task.creator.id:
                    check = True
                participants = task.participants.split(",")
                for participant in participants:
                    participant = participant.strip()
                    if str(user_id) == participant:
                        check = True
                if not check:
                    return JsonResponse(
                        ErrorResponse(errors="User is not creator or participant of this task").to_dict()
                    )

        except Exception as e:
            return JsonResponse(
                        ErrorResponse(errors=str(e)).to_dict()
                    )
        return None