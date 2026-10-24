from django.db import models
from django.urls import reverse


class Section(models.Model):
    """Раздел: Мошенники, Звонки, Игры, Сообщения..."""
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('URL', unique=True)
    icon = models.CharField('Иконка (эмодзи)', max_length=10, default='🛡️')
    short_description = models.CharField('Краткое описание', max_length=300)
    color = models.CharField('Цвет (hex)', max_length=7, default='#4f46e5')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('section', args=[self.slug])


class Article(models.Model):
    """Статья внутри раздела"""
    section = models.ForeignKey(Section, related_name='articles',
                                on_delete=models.CASCADE, verbose_name='Раздел')
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержимое (HTML)')
    image = models.ImageField('Картинка', upload_to='articles/', blank=True, null=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    """Вопрос для викторины"""
    question = models.CharField('Вопрос', max_length=300)
    explanation = models.TextField('Объяснение после ответа', blank=True)

    def __str__(self):
        return self.question


class QuizAnswer(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='answers',
                                 on_delete=models.CASCADE)
    text = models.CharField('Текст ответа', max_length=200)
    is_correct = models.BooleanField('Правильный', default=False)

    def __str__(self):
        return f'{self.text} ({"✓" if self.is_correct else "✗"})'
    
    
# core/models.py — добавь

class Quest(models.Model):
    """Интерактивный квест с ветвлением сюжета"""
    title = models.CharField('Название квеста', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание для карточки')
    icon = models.CharField('Иконка (эмодзи)', max_length=10, default='🎭')
    color = models.CharField('Цвет карточки', max_length=7, default='#8b5cf6')
    order = models.PositiveIntegerField('Порядок', default=0)
    start_scene = models.ForeignKey(
        'QuestScene',
        related_name='+',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Стартовая сцена'
    )

    class Meta:
        ordering = ['order']
        verbose_name = 'Квест'
        verbose_name_plural = 'Квесты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('quest_detail', args=[self.slug])


class QuestScene(models.Model):
    """Сцена (ситуация) внутри квеста"""
    quest = models.ForeignKey(Quest, related_name='scenes',
                              on_delete=models.CASCADE, verbose_name='Квест')
    title = models.CharField('Заголовок сцены', max_length=200)
    text = models.TextField('Текст ситуации (можно HTML)')
    is_ending = models.BooleanField('Финальная сцена', default=False)
    ending_type = models.CharField(
        'Тип финала', max_length=10, blank=True,
        choices=[
            ('good', '✅ Хороший'),
            ('bad', '❌ Плохой'),
            ('neutral', '🤔 Нейтральный'),
        ]
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Сцена квеста'
        verbose_name_plural = 'Сцены квестов'

    def __str__(self):
        return f'{self.quest.title} — {self.title}'


class QuestChoice(models.Model):
    """Вариант выбора в сцене"""
    scene = models.ForeignKey(QuestScene, related_name='choices',
                              on_delete=models.CASCADE, verbose_name='Сцена')
    text = models.CharField('Текст выбора', max_length=200)
    next_scene = models.ForeignKey(
        QuestScene, related_name='+',
        on_delete=models.CASCADE,
        verbose_name='Ведёт к сцене'
    )
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Вариант выбора'
        verbose_name_plural = 'Варианты выбора'

    def __str__(self):
        return self.text