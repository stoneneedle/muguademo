from django.contrib.auth.models import User
from django.db import models

# Custom User Models

# Assignments
class Assignment(models.Model):
    title = models.CharField(max_length=120)
    
    max_grade_pts = models.IntegerField(default=100)
    description = models.TextField()

    def __str__(self):
        return self.title

# Discussions
class Discussion(models.Model):
    title = models.CharField(max_length=120)
    message = models.TextField()
    post_date = models.DateTimeField()

    def __str__(self):
        return self.title

# TDL / Tutorial Models
class ToDoList(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text