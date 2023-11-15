from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class QuestionManager(models.Manager):
    pass


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    tags = models.ManyToManyField('Tag')
    likes = models.PositiveIntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    date_written = models.DateField()
    objects = QuestionManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_image = models.ImageField(max_length=255, default='messi.jpg')


class Answer(models.Model):
    parent_question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.PositiveIntegerField()
    date_written = models.DateField(null=True)


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
