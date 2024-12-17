from rest_framework import generics
from django.http import JsonResponse

from .models import Tasklists
from .serializers import TasklistsSerializer
from work_management.responses import ResponseObject, ErrorResponse
from work_management.utils import send_Email, get_user_from_request
from work_management.settings import EMAIL_HOST_USER
from tasks.models import Tasks
from tasks.serializers import TasksSerializer
from work_management.utils import send_Email

# Create your views here.
class TaskListsView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        tasklists = Tasklists.objects.all()
        tasklists_serializer = TasklistsSerializer(tasklists, many=True)
        return JsonResponse(
            ResponseObject(code=200, data=tasklists_serializer.data).to_dict()
        )


class CreateTask(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        tasklist_id = kwargs.get("id")
        if not tasklist_id:
            return JsonResponse(ErrorResponse(errors="Missing task list id").to_dict())

        tasks_serializer = TasksSerializer(data=request.data)
        if tasks_serializer.is_valid():
            try:
                Tasks.objects.create(
                    name=request.data.get("name"),
                    creator_id=request.data.get("creator"),
                    tasklist_id=tasklist_id,
                    status=request.data.get("status"),
                    comment=request.data.get("comment", ""),
                    participants=request.data.get("participants", ""),
                )
                
                user = get_user_from_request(request)
                email = user.email
                send_Email(email, EMAIL_HOST_USER, "Successfully create task", "Create task notification")

                return JsonResponse(
                    ResponseObject(
                        code=201, message="Create task successfully"
                    ).to_dict()
                )
            except Exception as e:
                return JsonResponse(ErrorResponse(errors=str(e)).to_dict())
        else:
            return JsonResponse(
                ErrorResponse(errors=str(tasks_serializer.errors)).to_dict()
            )
