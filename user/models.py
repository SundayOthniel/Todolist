from django.utils import timezone
from django.db import models
from adminUser.models import User

class Todo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    title =models.CharField(max_length=300)
    description = models.TextField(max_length=10000)
    due_date = models.DateField()
    priority = models.TextField(max_length=6)
    status = models.TextField(max_length=11)
    creationDate = models.DateTimeField(default=timezone.now, editable=False)
    update = models.DateTimeField(auto_now=True)
    
    
    