import random
from django.core.management.base import BaseCommand
from mimesis import Person
from mimesis.locales import Locale
from app.models import User, Question, Tag, Answer, Profile
from django.contrib.auth.models import User
from mimesis import Text
from datetime import datetime, timedelta
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fill database with randomized content'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Indicates the number of rows to be created')

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, Profile, Question, Answer, Tag]
        for m in models:
            m.objects.all().delete()


        ratio = kwargs['ratio']

        _fill_users(ratio)
        _fill_tags(ratio)
        _fill_questions(ratio * 10)
        _fill_answers(ratio * 100)
        # _fill_likes(ratio * 500)


def _fill_users(ratio):
    print('Creating users...')
    users = []
    for _ in range(ratio):
        person = Person(Locale.EN)

        u = User(first_name=person.first_name(),
                 last_name=person.last_name(),
                 email=person.email(),
                 password=person.password(),
                 is_staff=False,
                 username=person.username(),
                 )

        users.append(u)

    User.objects.bulk_create(users, ignore_conflicts=True)

    persisted_users = User.objects.all()
    profiles = []
    for user in persisted_users:
        profiles.append(Profile(user=user))
    Profile.objects.bulk_create(profiles, ignore_conflicts=False)


def _fill_tags(ratio):
    print('Creating tags...')
    tags = []
    for _ in range(ratio):
        txt = Text(Locale.EN)

        t = Tag(name=txt.word())
        tags.append(t)
    Tag.objects.bulk_create(tags, ignore_conflicts=True)


def _fill_questions(ratio):
    print('Creating questions...')

    users = list(User.objects.all())
    random.shuffle(users)

    questions = []
    for i in range(ratio):
        txt = Text(Locale.EN)

        q = Question(title=txt.quote(),
                     content=txt.text(5),
                     author=users[i % (len(users) or 1)],
                     likes=random.randint(0, 100),
                     date_written=datetime.now()-timedelta(hours=random.randint(0, 1000)))

        questions.append(q)

    Question.objects.bulk_create(questions, ignore_conflicts=False)

    persisted_questions = Question.objects.all()

    all_tags = Tag.objects.all()
    for i in range(ratio):
        persisted_questions[i].tags.set(random.sample(list(all_tags), random.randint(0, 3)))
        persisted_questions[i].save()


def _fill_answers(ratio):
    print('Creating answers...')

    users = list(User.objects.all())
    random.shuffle(users)
    questions = list(Question.objects.all())
    random.shuffle(questions)

    n = 10
    for j in range(n):
        print(f'Creating answers #{j+1}...')
        answers = []
        for i in range(ratio // n):
            txt = Text(Locale.EN)
            a = Answer(content=txt.text(5),
                       author=users[i % (len(users) or 1)],
                       parent_question=questions[i % (len(questions) or 1)],
                       likes=random.randint(0, 100))
            answers.append(a)
        Answer.objects.bulk_create(answers, ignore_conflicts=True)


# def _fill_likes(ratio):
#     for _ in range(ratio):
#         users = list(User.objects.all())
#         questions = list(Question.objects.all())
#         answers = list(Answer.objects.all())
#
#         random_user = random.choice(users)
#         random_question = random.choice(questions)
#         random_answer = random.choice(answers)
#
#         random_question.likes.set(random_user)
#         random_answer.likes.add(random_user)
