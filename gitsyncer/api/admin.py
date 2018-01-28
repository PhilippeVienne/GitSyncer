from django.contrib import admin

from gitsyncer.api.models import Mirror, Repository, SSHKey


@admin.register(Mirror)
class MirrorAdmin(admin.ModelAdmin):

    list_display = ('id', 'origin', 'destination', 'owner')
    search_fields = ('origin__name', 'destination__name')


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'remote_url')
    search_fields = ('name', 'remote_url')


@admin.register(SSHKey)
class SSHKeyAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'public_key')
    search_fields = ('id',)

    def get_changeform_initial_data(self, request):
        return SSHKey.gen_keys()
