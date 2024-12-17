from django.urls import path

from .views import *

urlpatterns = [
    path('', TaskListsView.as_view()),
    path('<int:id>/tasks', CreateTask.as_view()),
]