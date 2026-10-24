from django.contrib import admin
from .models import QuestChoice, Section, Article, QuizQuestion, QuizAnswer, QuestScene, Quest


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 1


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'order', 'color')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ArticleInline]


class AnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 3


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    
class QuestChoiceInline(admin.TabularInline):
    model = QuestChoice
    fk_name = 'scene'
    extra = 2
    autocomplete_fields = ['next_scene']


@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'order', 'start_scene')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('order',)
    search_fields = ('title',)


@admin.register(QuestScene)
class QuestSceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'quest', 'is_ending', 'ending_type')
    list_filter = ('quest', 'is_ending', 'ending_type')
    search_fields = ('title', 'text')
    inlines = [QuestChoiceInline]