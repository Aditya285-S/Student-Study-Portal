from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'notes'
        verbose_name_plural = 'notes'

    def __str__(self):
        return self.title
    

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    due = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.subject


class ToDo(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50)
    time = models.TimeField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todo'

    def __str__(self):
        return self.title