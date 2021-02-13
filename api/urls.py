from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (TaskViewSet, TagViewSet, CategoryViewSet,
                    TaskHistoryViewSet, TaskHistoryDownload, TasksDownload,
                    upload, send, )
                    
from django.views.generic import TemplateView

task_history = TaskHistoryViewSet.as_view(
    {
        'get': 'list',
    }
)
tasks_download = TasksDownload.as_view(
    {
        'get': 'list',
    }
)
task_history_download = TaskHistoryDownload.as_view(
    {
        'get': 'list',
    }
)

v1_router = DefaultRouter()

v1_router.register('tasks', TaskViewSet, basename=TaskViewSet)
v1_router.register('tags', TagViewSet, basename=TagViewSet)
v1_router.register('categories', CategoryViewSet, basename=CategoryViewSet)

urlpatterns = [
    path('v1/redoc/', TemplateView.as_view(template_name='redoc.html'), name='redoc'),
    path('v1/tasks/download/', tasks_download, name='task-download'),
    path('v1/tasks/upload/', upload, name='task-upload'),
    path('v1/tasks/send/', send, name='task-send'),
    path('v1/tasks/<int:pk>/history/', task_history, name='task-history'),
    path('v1/tasks/<int:pk>/history/download/', task_history_download, name='task-history-download'),
    path('v1/', include(v1_router.urls), name='v1'),
]
