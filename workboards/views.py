from rest_framework import generics
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage

from .models import Workboards
from .serializers import WorkboardsSerializer
from work_management.responses import ResponseObject, ErrorResponse
from users.models import User
from users.serializers import UserSerializer
from tasklists.models import Tasklists
from tasklists.serializers import TasklistsSerializer

# Create your views here.


class WorkboardsListView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        if request.GET.get("workboard"):
            workboards = Workboards.objects.filter(name__contains=request.GET.get("workboard"))
        else:
            workboards = Workboards.objects.all()

        paginator = Paginator(workboards, 5)
        page = request.GET.get("page", 1)

        try:
            workboards_page = paginator.page(page)
        except EmptyPage:
            workboards_page = paginator.page(paginator.num_pages)

        workboards_serializer = [WorkboardsSerializer(workboard).data for workboards in workboards_page]
        return JsonResponse(
            ResponseObject(code=200, data=workboards_serializer).to_dict()
        )

    def post(self, request, *args, **kwargs):
        workboards_serializer = WorkboardsSerializer(data=request.data)
        if workboards_serializer.is_valid():
            Workboards.objects.create(
                name=request.data.get("name"), creator_id=request.data.get("creator")
            )
            return JsonResponse(
                ResponseObject(
                    code=201, message="Create workboard successfully"
                ).to_dict()
            )
        else:
            return JsonResponse(
                ErrorResponse(errors=str(workboards_serializer.errors)).to_dict()
            )


class CreateTaskList(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        workboard_id = kwargs.get("id")
        if not workboard_id:
            return JsonResponse(ErrorResponse(errors="Missing workboard id").to_dict())
        tasklists_serializer = TasklistsSerializer(data=request.data)
        if tasklists_serializer.is_valid():
            Tasklists.objects.create(
                name=request.data.get("name"),
                creator_id=request.data.get("creator"),
                workboard_id=int(workboard_id),
            )
            return JsonResponse(
                ResponseObject(
                    code=201, message="Create task list successfully"
                ).to_dict()
            )
        else:
            return JsonResponse(
                ErrorResponse(errors=str(tasklists_serializer.errors)).to_dict()
            )
