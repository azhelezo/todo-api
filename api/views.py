from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import redirect
from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse, FileResponse
from datetime import datetime as dt
import requests
import csv
from todo.settings import DATETIME_FORMAT

from rest_framework_csv import renderers as r

from tasks.models import Task, Tag, Category
from .serializers import (TaskSerializer, TagSerializer, CategorySerializer,
                          TaskHistorySerializer)


@api_view(['POST', 'PUT', ])
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


@api_view(['GET', ])
def send(request):
    url = 'http://qa-test.expsys.org:8080/upload-file'
    #url2 = 'https://httpbin.org/anything'
    queryset = Task.objects.all()
    serializer = TaskSerializer
    data = serializer(queryset, many=True)
    renderer = r.CSVRenderer()
    file_text = (renderer.render(data.data).decode())
    files = {'file': ('send.csv', file_text)}
    re = requests.post(url, files=files, )
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
