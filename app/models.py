from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class QuestionManager(models.Manager):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nickname = models.CharField(max_length=255, null=True)
    profile_image = models.ImageField(default='messi.jpg')


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    tags = models.ManyToManyField('Tag')
    likes = models.PositiveIntegerField(default=0)
    # likes = models.ManyToManyField(Profile, related_name='liked_questions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', null=True)
    date_written = models.DateField(null=True)
    objects = QuestionManager()


class Answer(models.Model):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # likes = models.PositiveIntegerField(default=0)
    date_written = models.DateField(null=True)
    likes = models.ManyToManyField(User, related_name='liked_answers')


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)