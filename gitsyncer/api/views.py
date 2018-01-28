from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from gitsyncer.api.models import Mirror


class SyncView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, token, format=None):
        try:
            mirror = Mirror.objects.get(token=token)
        except Mirror.DoesNotExist:
            raise Http404
        mirror.sync()
        return Response({'success': True})
