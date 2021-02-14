import requests
from datetime import datetime as dt
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_csv import renderers as r
from tasks.models import Category, Tag, Task
from todo.settings import DATETIME_FORMAT
from .serializers import (CategorySerializer, TagSerializer,
                          TaskHistorySerializer, TaskSerializer)

UPLOAD_URL = 'https://httpbin.org/anything'  # 'http://qa-test.expsys.org:8080/upload-file'


@api_view(['POST', ])
def upload(request):
    if (
            len(request.FILES) == 0 or
            not request.FILES['file'].name.endswith('.csv')
            ):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    data = request.FILES['file'].readlines()
    out = []
    for row in data:
        vals = row.decode().rstrip().split(',')
        now = dt.now().strftime(DATETIME_FORMAT)
        data = {
            'text': ''.join(vals[0:1]),
            'deadline': ''.join(vals[1:2]),
            'category': ''.join(vals[2:3]),
            'tags': vals[3:],
            'created': now,
            'updated': now,
        }
        cat, created = Category.objects.get_or_create(pk=data['category'])
        data['category'] = cat.name
        for tag in data['tags']:
            tag, created = Tag.objects.get_or_create(pk=tag)
            tag = tag.name
        out.append(data)
    serializer = TaskSerializer(data=out, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(out)


@api_view(['POST', ])
def send(request):
    queryset = Task.objects.all()
    serializer = TaskSerializer
    data = serializer(queryset, many=True)
    renderer = r.CSVRenderer()
    file_text = (renderer.render(data.data).decode())
    files = {'file': ('send.csv', file_text)}
    re = requests.post(UPLOAD_URL, files=files, )
    return Response(re.json())


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

    def get_queryset(self):
        name = self.kwargs.get('pk', None)
        queryset = Task.objects.filter(tags__name=name)
        if queryset:
            return queryset
        return Tag.objects.all()

    def get_serializer_class(self):
        name = self.kwargs.get('pk', None)
        if name is not None:
            return TaskSerializer
        return TagSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(queryset, many=True)
        return Response(data.data)


class CategoryViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        name = self.kwargs.get('pk', None)
        if name is None:
            return Category.objects.all()
        queryset = Task.objects.filter(category=name)
        return queryset

    def get_serializer_class(self):
        name = self.kwargs.get('pk', None)
        if name is not None:
            return TaskSerializer
        return CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        data = serializer(queryset, many=True)
        return Response(data.data)
