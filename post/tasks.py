from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import Story
from celery.schedules import crontab
# from celery.task import periodic_task
from django.utils import timezone
from celery import shared_task

from post.models import Story
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

@shared_task
def delete_old_stories():
    # Calculate the timestamp 24 hours ago
    threshold = timezone.now() - timedelta(hours=24)
    
    # Delete stories older than 24 hours
    old_stories = Story.objects.filter(created_on__lte=threshold)
    old_stories.delete()

@shared_task
def delete_old_stories():
    # Calculate the timestamp 24 hours ago
    print('--------------------------->>>>>>in celry function-------------------')
    threshold = timezone.now() - timedelta(hours=24)
    # Delete stories older than 24 hours
    old_stories = Story.objects.filter(created_on__lte=threshold)
    for story in old_stories:
        story.visible=False
        story.save()
        print('---------------saved-----------------')
        
    # .__init__.py
    # from firpta.celery import app as celery_app

    # __all__ = ("celery_app",)
