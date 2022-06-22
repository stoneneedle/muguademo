from django.contrib.auth.models import User
from django.db import models

# Custom User Models

# LMS Models
class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacherscourse", null=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="asmtcourse", null=True)
    title = models.CharField(max_length=120)
    max_grade_pts = models.IntegerField(default=100)
    description = models.TextField()
    
    def __str__(self):
        return self.title

# Discussions
class Discussion(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="discusscourse", null=True)
    author = models.CharField(max_length=120, null=True)
    title = models.CharField(max_length=120, null=True)
    message = models.TextField(null=True)
    post_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussion", null=True)

    def __str__(self):
        return self.title

class DiscussionReply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="discussionreply", null=True)
    author = models.CharField(max_length=120, null=True)
    title = models.CharField(max_length=120, null=True)
    message = models.TextField(null=True)
    post_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userreply", null=True)

    def __str__(self):
        return self.message

# TDL / Tutorial Models
class ToDoList(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="todolist", null=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text