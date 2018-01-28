import binascii
import os
import stat

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models
from django.utils.translation import ugettext_lazy as _
from git import Repo, Git


class SSHKey(models.Model):
    private_key = models.TextField(blank=True)
    public_key = models.TextField(blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.private_key is None or self.private_key == '':
            key = self.gen_keys()
            self.private_key = key['private_key']
            self.public_key = key['public_key']
            pass

    @staticmethod
    def gen_keys():
        key = rsa.generate_private_key(
            backend=crypto_default_backend(),
            public_exponent=65537,
            key_size=2048
        )
        return {
            'private_key':
                (key.private_bytes(
                    crypto_serialization.Encoding.PEM,
                    crypto_serialization.PrivateFormat.PKCS8,
                    crypto_serialization.NoEncryption())).decode('utf-8'),
            'public_key':
                (key.public_key().public_bytes(
                    crypto_serialization.Encoding.OpenSSH,
                    crypto_serialization.PublicFormat.OpenSSH
                )).decode('utf-8')
        }

    def __str__(self):
        return "SSH-{}".format(self.pk)

    def get_file(self):
        ssh_file = self._get_path()
        with open(ssh_file, "w") as text_file:
            text_file.write(self.private_key)
        os.chmod(ssh_file, stat.S_IRWXU)
        return ssh_file

    def _get_path(self):
        return os.path.join(settings.CLONE_ROOT, ".id_ssh_%s" % self.pk)


class Repository(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('nom'))
    remote_url = models.CharField(max_length=2500, verbose_name=_('url du dépot'))
    ssh_key = models.ForeignKey(SSHKey, on_delete=models.PROTECT, null=True, blank=True)

    def get_ssh_command(self):
        if self.ssh_key_id is None:
            return 'ssh'
        else:
            return 'ssh -o IdentitiesOnly=yes -i %s' % self.ssh_key.get_file()

    def __str__(self):
        return "{} ({})".format(self.name, self.remote_url)


def random_token():
    return binascii.hexlify(os.urandom(18)).decode('utf-8')


class Mirror(models.Model):
    token = models.CharField(max_length=250, verbose_name=_('clef'), unique=True, default=random_token)
    origin = models.ForeignKey(Repository, verbose_name=_('origine'), on_delete=models.CASCADE,
                               related_name='mirrors_as_origin')
    destination = models.ForeignKey(Repository, verbose_name=_('destination'), on_delete=models.CASCADE,
                                    related_name='mirrors_as_destination')
    enabled = models.BooleanField(verbose_name=_('activé'), default=True)
    owner = models.ForeignKey(Group, verbose_name=_('propriétaire'), on_delete=models.PROTECT)
    last_sync = models.DateTimeField(verbose_name=_('dernière synchronisation'), null=True, blank=True)

    def sync(self):
        os.makedirs(settings.CLONE_ROOT, exist_ok=True)
        path = os.path.join(settings.CLONE_ROOT, str(self.pk))
        origin_env = dict(GIT_SSH_COMMAND=self.origin.get_ssh_command())
        destination_env = dict(GIT_SSH_COMMAND=self.destination.get_ssh_command())
        if not os.path.exists(path):
            repo = Repo.clone_from(self.origin.remote_url, path, mirror=True, env=origin_env)
            origin = repo.remote('origin')
        else:
            repo = Repo(path)
            origin = repo.remote('origin')
        try:
            dest_remote = repo.remote('destination')
        except ValueError:
            dest_remote = repo.create_remote('destination', self.destination.remote_url, env=destination_env)
        origin.update(env=origin_env)
        dest_remote.push(mirror=True, env=destination_env)
