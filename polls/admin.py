from django.contrib import admin
from .models import Question, Choice, Vote  # Добавляем Vote
from import_export.admin import ImportExportModelAdmin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ('question_text', 'pub_date', 'end_date', 'was_published_recently', 'is_active')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']
    inlines = [ChoiceInline]
    date_hierarchy = 'pub_date'

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'votes')
    list_filter = ['question']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice')
    list_filter = ['question']

admin.site.site_header = "Панель администратора опросов"
admin.site.index_title = "Добро пожаловать!"