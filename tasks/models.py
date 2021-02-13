from django.db import models
from simple_history.models import HistoricalRecords


class Label(models.Model):
    name = models.SlugField('Название', primary_key=True, allow_unicode=True)
    search_fields = ['name']

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['name']


class Tag(Label):
    pass


class Category(Label):
    pass


class Task(models.Model):
    text = models.TextField('Цель', blank=False, null=False)

    deadline = models.DateTimeField('Срок исполнения', null=True, blank=True)
    created = models.DateTimeField('Начало', auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField('Последнее изменение', auto_now=True, null=True, blank=True)

    done = models.BooleanField('Выполнено', default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories',
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        blank=True,
        verbose_name='Метки',
    )
    history = HistoricalRecords(cascade_delete_history=True)

    def __str__(self):
        return self.text[:20]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created', ]
        else:
            return []

    class Meta:
        ordering = ['done', '-deadline', ]
