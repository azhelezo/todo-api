from django.shortcuts import render, redirect
from rest_framework.decorators import action
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse

from tasks.models import Task, Tag, Category
from .serializers import TaskSerializer, TagSerializer, CategorySerializer, TaskHistorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, validated_data):
        task, created = Task.objects.update_or_create(data=validated_data)
        return task


class TaskHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        queryset = Task.history.filter(id=id)
        if queryset:
            return queryset
        return redirect('home')


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
