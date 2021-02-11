from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Tag, Category, Task


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )
    empty_value_display = '-пусто-'


class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'deadline', 'created', 'updated', 'category', 'done',)
    search_fields = ('text', )
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
#admin.site.register(Task, TaskAdmin)
admin.site.register(Task, SimpleHistoryAdmin)
