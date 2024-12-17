from django.db import models
from rest_framework.pagination import PageNumberPagination

from users.models import User
from tasklists.models import Tasklists
# Create your models here.

STATUS = [
    ("1", "Done"),
    ("2", "Progressing"),
    ("3", "On Hold"),
    ("4", "Failed")
]

class Tasks(models.Model):
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tasklist = models.ForeignKey(Tasklists, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default="2", choices=STATUS)
    participants = models.TextField(default="", blank=True, null=True)

class SmallPagesPagination(PageNumberPagination):  
    page_size = 5