from rest_framework import serializers

from tasks.models import Tag, Category, Task, TaskHistory


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskHistory
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'