from django.db import models


class Label(models.Model):
    name = models.SlugField(primary_key=True, allow_unicode=True, verbose_name='Название')
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


class BaseTask(models.Model):
    text = models.TextField(verbose_name='Цель', blank=False, null=False)

    deadline = models.DateTimeField(verbose_name='Срок исполнения', blank=True, null=True)
    created = models.DateTimeField(verbose_name='Начало', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Последнее изменение', auto_now=True)

    done = models.BooleanField(verbose_name='Выполнено', default=False)

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

    def __str__(self):
        return self.text[:20]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['created', ]
        else:
            return []

    class Meta:
        ordering = ['-deadline']


class Task(BaseTask):
    pass


class TaskHistory(BaseTask):
    parent = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='original',
        verbose_name='История',
        )

    class Meta:
        ordering = ['-updated']
