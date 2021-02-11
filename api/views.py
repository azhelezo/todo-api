from django.shortcuts import render

from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from tasks.models import Task, TaskHistory, Tag, Category
from .serializers import TaskSerializer, TaskHistorySerializer, TagSerializer, CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskHistoryViewSet(viewsets.ModelViewSet):
    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
