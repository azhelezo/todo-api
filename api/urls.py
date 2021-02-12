from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TagViewSet, CategoryViewSet, TaskHistoryViewSet

task_history = TaskHistoryViewSet.as_view(
    {
        'get': 'list',
    }
)

v1_router = DefaultRouter()

v1_router.register('tasks', TaskViewSet, basename=TaskViewSet)
v1_router.register('tags', TagViewSet, basename=TagViewSet)
v1_router.register('categories', CategoryViewSet, basename=CategoryViewSet)

urlpatterns = [
    path('v1/tasks/<int:pk>/history/', task_history, name='task-history'),
    path('v1/', include(v1_router.urls), name='v1'),
]
