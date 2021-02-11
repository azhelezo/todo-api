from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaseTask, Task, TaskHistory
from api.serializers import TaskSerializer, TaskHistorySerializer


@receiver(post_save, sender=Task)
def update_task(sender, instance, **kwargs):
    deserializer = TaskSerializer(instance=instance)
    data = deserializer.data
    data['parent'] = instance.id
    print(data)
    serializer = TaskHistorySerializer(data=data)
    serializer.is_valid()
    serializer.save()
