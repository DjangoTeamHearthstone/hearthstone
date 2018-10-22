from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=200)

class Member(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.username