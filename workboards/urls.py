from django.urls import path

from .views import *

urlpatterns = [
    path('', WorkboardsListView.as_view()),
    path('<int:id>/tasklists', CreateTaskList.as_view()),
]