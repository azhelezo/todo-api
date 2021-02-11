from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, TaskHistoryViewSet, TagViewSet, CategoryViewSet

v1_router = DefaultRouter()

v1_router.register('tasks', TaskViewSet, basename=TaskViewSet)
v1_router.register('task_history', TaskHistoryViewSet, basename=TaskHistoryViewSet)
v1_router.register('tags', TagViewSet, basename=TagViewSet)
v1_router.register('categories', CategoryViewSet, basename=CategoryViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
