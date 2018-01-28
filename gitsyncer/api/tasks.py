from __future__ import absolute_import, unicode_literals
from celery import shared_task

from gitsyncer.api.models import Mirror


@shared_task
def sync_repo(pk):
    Mirror.objects.get(pk=pk).sync()
    return True
