from django.contrib import admin

from gitsyncer.api.models import Mirror


@admin.register(Mirror)
class MirrorAdmin(admin.ModelAdmin):
    pass
