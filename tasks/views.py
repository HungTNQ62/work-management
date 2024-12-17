from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

from work_management.responses import ResponseObject, ErrorResponse
from work_management.utils import send_Email, get_user_from_request
from work_management.settings import EMAIL_HOST_USER
from .models import Tasks
from .serializers import TasksSerializer
from comment.models import Comment
from comment.serializers import CommentSerializer
from attachment.serializers import AttachmentSerializer
from attachment.models import Attachment

# Create your views here.


class TasksView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get("task"):
            tasks = Tasks.objects.filter(name__contains=request.GET.get("task"))
        else:
            tasks = Tasks.objects.all()

        paginator = Paginator(tasks, 5)
        page = request.GET.get("page", 1)

        try:
            tasks_page = paginator.page(page)
        except EmptyPage:
            tasks_page = paginator.page(paginator.num_pages)

        tasks_serializer = [TasksSerializer(task).data for task in tasks_page]
        return JsonResponse(
            ResponseObject(code=200, data=tasks_serializer).to_dict()
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    def patch(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        if not task_id:
            return JsonResponse(ErrorResponse(errors="Missing task id").to_dict())

        try:
            task = Tasks.objects.get(id=task_id)
            task.status = request.data.get("status", "2")
            task.save()
            user = get_user_from_request(request)
            email = user.email
            send_Email(email, EMAIL_HOST_USER, "Successfully update status for task " + str(task_id), "Update status notification")
            return JsonResponse(
                ResponseObject(message="Update task status successfully").to_dict()
            )
        except Exception as e:
            return JsonResponse(ErrorResponse(errors=str(e)).to_dict())

    def delete(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        if not task_id:
            return JsonResponse(ErrorResponse(errors="Missing task id").to_dict())

        try:
            task = Tasks.objects.get(id=task_id)
            task.delete()
            user = get_user_from_request(request)
            email = user.email
            send_Email(email, EMAIL_HOST_USER, "Successfully delete task " + str(task_id), "Delete task notification")
            return JsonResponse(
                ResponseObject(code=204, message="Delete task successfully").to_dict()
            )
        except Exception as e:
            return JsonResponse(ErrorResponse(errors=str(e)).to_dict())


class TaskAddComment(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        if not task_id:
            return JsonResponse(ErrorResponse(errors="Missing task id").to_dict())

        if not request.data.get('comment') or not request.data.get('creator'):
            return JsonResponse(ErrorResponse(errors="Missing comment or creator").to_dict())
        try:
            new_comment = Comment.objects.create(comment=request.data.get('comment'), creator_id=request.data.get('creator'), task_id=task_id)
            return JsonResponse(
                ResponseObject(data=CommentSerializer(new_comment).data, message="Add comment successfully").to_dict()
            )
        except Exception as e:
            return JsonResponse(ErrorResponse(errors=str(e)).to_dict())

class TaskAddAttachment(generics.CreateAPIView):
    parsers_classes = (FormParser, MultiPartParser, JSONParser)
    def post(self, request, *args, **kwargs):
        task_id = kwargs.get("id")
        if not task_id:
            return JsonResponse(ErrorResponse(errors="Missing task id").to_dict())
        
        try:
            serializer = AttachmentSerializer(data=request.data)
            if serializer.is_valid():
                Attachment.objects.create(name=request.data.get('name'), creator_id=request.data.get('creator'), task_id=task_id, file=request.data.get('file'))
                return JsonResponse(
                    ResponseObject(data=serializer.data, message="Add attachment successfully").to_dict()
                )
            return JsonResponse(ErrorResponse(errors="Something is wrong").to_dict())
        except Exception as e:
            return JsonResponse(ErrorResponse(errors=str(e)).to_dict())