from django.shortcuts import render, get_object_or_404
from .models import Section, QuizQuestion, Quest, QuestScene
from django.shortcuts import render, get_object_or_404, redirect
from .models import Section, QuizQuestion, Quest, QuestScene

def home(request):
    sections = Section.objects.all()
    return render(request, 'core/home.html', {'sections': sections})


def section_detail(request, slug):
    section = get_object_or_404(Section, slug=slug)
    articles = section.articles.all()
    return render(request, 'core/section.html', {
        'section': section,
        'articles': articles,
    })


from django.shortcuts import render
from .models import QuizQuestion


def quiz(request):
    questions_qs = QuizQuestion.objects.prefetch_related('answers').all()

    questions = []
    for q in questions_qs:
        answers = list(q.answers.all())
        correct_index = next(
            (i for i, a in enumerate(answers) if a.is_correct),
            0,
        )
        questions.append({
            'id': q.id,
            'question': q.question,
            'explanation': q.explanation,
            'answers': answers,
            'correct_index': correct_index,
        })

    return render(request, 'core/quiz.html', {'questions': questions})

from .models import Quest, QuestScene


def quest_list(request):
    quests = Quest.objects.all()
    return render(request, 'core/quest_list.html', {'quests': quests})


def quest_detail(request, slug):
    quest = get_object_or_404(Quest, slug=slug)
    if not quest.start_scene:
        return render(request, 'core/quest_error.html', {'quest': quest})
    return redirect('quest_scene', slug=quest.slug, scene_id=quest.start_scene.id)


def quest_scene(request, slug, scene_id):
    quest = get_object_or_404(Quest, slug=slug)
    scene = get_object_or_404(QuestScene, id=scene_id, quest=quest)
    return render(request, 'core/scene.html', {
        'quest': quest,
        'scene': scene,
    })