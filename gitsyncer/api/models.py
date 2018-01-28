import os

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from git import Repo


class Mirror(models.Model):
    origin = models.CharField(max_length=250, verbose_name=_('origine'))
    destination = models.CharField(max_length=250, verbose_name=_('destination'))
    enabled = models.BooleanField(verbose_name=_('activé'), default=True)
    last_sync = models.DateTimeField(verbose_name=_('dernière synchronisation'), null=True, blank=True)

    def sync(self):
        path = os.path.join(settings.CLONE_ROOT, str(self.pk))
        if not os.path.exists(path):
            repo = Repo.clone_from(self.origin, path, mirror=True)
            origin = repo.remote('origin')
        else:
            repo = Repo(path)
            origin = repo.remote('origin')
        try:
            dest_remote = repo.remote('destination')
        except ValueError:
            dest_remote = repo.create_remote('destination', self.destination)
        origin.update()
        dest_remote.push(mirror=True)
