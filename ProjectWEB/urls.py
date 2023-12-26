"""
URL configuration for ProjectWEB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('best-questions', views.best_questions, name='best-questions'),
    path('new-questions', views.new_questions, name='new-questions'),
    path('question/<str:id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('settings', views.settings, name='settings'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('tag/<str:name>', views.tag, name='tag'),
    path('logout', views.user_logout, name='user_logout'),
    path('admin/', admin.site.urls),
]
