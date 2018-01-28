from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from gitsyncer.api.models import Mirror


class SyncView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request, token, format=None):
        """
        Return a list of all users.
        """
        mirror = Mirror.objects.get(token=token)
        mirror.sync()
        return Response(str(mirror.id))
