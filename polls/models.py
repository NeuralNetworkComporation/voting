from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # Добавляем импорт User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', null=True, blank=True)  # Добавим дедлайн

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def is_active(self):
        """Проверяет, активно ли ещё голосование"""
        now = timezone.now()
        return self.pub_date <= now <= self.end_date if self.end_date else True


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # Меняем poll на question
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')  # Один пользователь - один голос на вопрос


class Poll(models.Model):
    question = models.CharField(max_length=200)
    end_date = models.DateTimeField('дата окончания')