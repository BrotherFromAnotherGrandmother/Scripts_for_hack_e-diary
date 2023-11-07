import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

list_of_accolades = [
    'Молодец!',
    'Отлично!'
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def get_child(name):
    try:
        child = Schoolkid.objects.get(full_name__contains=name)
        return child
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned('Найдено несколько учеников, уточните ФИО')
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist(f"С именем '{name}' ничего не найдено")


def fix_marks(schoolkid):
    child = get_child(schoolkid)
    child_bad_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for child_bad_mark in child_bad_marks:
        child_bad_mark.points = 5
        child_bad_mark.save()


def remove_chastisements(schoolkid):
    child = get_child(schoolkid)
    child_chastisements = Chastisement.objects.filter(schoolkid=child)
    child_chastisements.delete()


def create_commendation(schoolkid: str, lesson: str, year_of_study: int, group_letter: str):
    child = get_child(schoolkid)
    all_given_lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
                                              subject__title=lesson)
    last_given_lesson = all_given_lessons.first()
    Commendation.objects.create(
        text=random.choice(list_of_accolades),
        created=last_given_lesson.date,
        schoolkid=child,
        subject=last_given_lesson.subject,
        teacher=last_given_lesson.teacher
    )
