from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse

from rest_framework_csv import renderers as r

from tasks.models import Task, Tag, Category
from .serializers import TaskSerializer, TagSerializer, CategorySerializer, TaskHistorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend, ]
    filterset_fields = ['category', 'tags', 'done', 'deadline', ]
    search_fields = ['text', ]
    ordering_fields = '__all__'


class TaskHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        queryset = Task.history.filter(id=id)
        if queryset:
            return queryset
        raise NotFound()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
