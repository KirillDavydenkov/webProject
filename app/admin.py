from django.contrib import admin

# Register your models here.
from .models import Question, Profile, Answer, Tag


admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(Tag)
