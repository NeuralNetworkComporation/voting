from django.utils import timezone  # Исправленный импорт timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {'questions': latest_question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):  # Убрана дублирующаяся функция vote
    question = get_object_or_404(Question, pk=question_id)

    # Проверяем, активно ли голосование
    if hasattr(question, 'end_date') and question.end_date < timezone.now():
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Голосование завершено!",
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "Вы не выбрали вариант ответа.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return redirect('polls:results', question_id=question.id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})