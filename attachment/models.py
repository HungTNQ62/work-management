from django.db import models

from tasks.models import Tasks
from users.models import User

# Create your models here.
class Attachment(models.Model):
    name = models.CharField(max_length=50, default='', null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, default='')
    file = models.FileField(upload_to='documents/', max_length=255, null=True, blank=True)