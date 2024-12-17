from django.urls import path

from .views import *

urlpatterns = [
    path('', TasksView.as_view()),
    path('<int:id>', TaskDetailView.as_view()),
    path('<int:id>/comment', TaskAddComment.as_view()),
    path('<int:id>/attachment', TaskAddAttachment.as_view()),
]