from rest_framework import serializers
from tasks.models import Category, Tag, Task
from todo.settings import DATETIME_FORMAT


class TaskSerializer(serializers.ModelSerializer):
    deadline = serializers.DateTimeField(format=DATETIME_FORMAT)
    created = serializers.DateTimeField(format=DATETIME_FORMAT, required=False)
    updated = serializers.DateTimeField(format=DATETIME_FORMAT, required=False)

    class Meta:
        model = Task
        fields = '__all__'


class TaskHistorySerializer(TaskSerializer):
    history_date = serializers.DateTimeField(format=DATETIME_FORMAT)

    class Meta:
        model = Task.history.model
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
