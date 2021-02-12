from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, FileResponse

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


class CSVDownloadMixin(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(queryset, many=True)
        renderer = r.CSVRenderer()
        response = HttpResponse(renderer.render(data.data), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'
        return response


class TasksDownload(TaskViewSet, CSVDownloadMixin):
    pass


class TaskHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = TaskHistorySerializer

    def get_queryset(self):
        id = self.kwargs.get('pk', None)
        queryset = Task.history.filter(id=id)
        if queryset:
            return queryset
        raise NotFound()


class TaskHistoryDownload(TaskHistoryViewSet, CSVDownloadMixin):
    pass


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
