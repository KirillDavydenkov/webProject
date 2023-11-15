from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Question, Tag, Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


def paginate(objects, request, per_page):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page', 1)
    try:
        page_items = paginator.page(page).object_list
    except PageNotAnInteger:
        page_items = paginator.page(1).object_list
    except EmptyPage:
        raise Http404("Страница не существует")
    return page_items


def get_tag(Tag):
    return Tag.objects.annotate(num_questions=Count('question')).order_by('-num_questions')[:10]


tags = get_tag(Tag=Tag)

def get_best_users(Profile):
     return Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]



# Create your views here.
def index(request):
    questions = Question.objects.all()
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'index.html',
                  {'questions': paginate(questions, request, per_page=10), 'tags': tags,
                   'best_users': best_users})


def best_questions(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    best_questions = Question.objects.all().exclude(likes=None).order_by("-likes")
    return render(request, 'index.html',
                  {'questions': paginate(best_questions, request, per_page=2), 'tags': tags,
                   'best_users': best_users})


def new_questions(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    new_questions = Question.objects.all().exclude(date_written=None).order_by("-date_written")
    return render(request, 'index.html',
                  {'questions': paginate(new_questions, request, per_page=2), 'tags': tags,
                   'best_users': best_users})


def question(request, id):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    question_object = Question.objects.get(id=id)
    return render(request, 'question.html',
                  {'tags': tags, 'question': question_object, 'best_users': best_users})


def tag(request, name):
    tag_object = Tag.objects.get(name=name)
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'tag.html',
                  {'tag': tag_object, 'tags': tags, 'best_users': best_users})


def ask(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'ask.html', {'tags': tags, 'best_users': best_users})


def settings(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'settings.html', {'tags': tags, 'best_users': best_users})


def login(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'login.html', {'tags': tags, 'best_users': best_users})


def register(request):
    best_users = Profile.objects.annotate(total_likes=Count('user__questions__likes') +
                                                      Count('user__answer__likes')).order_by(
        'total_likes')[:10]
    return render(request, 'register.html', {'tags': tags, 'best_users': best_users})
