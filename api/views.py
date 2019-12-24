from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings


class ValuesAPIView(APIView):
    def get(self, request):
        print("************************")
        print(settings.REDIS_HOST)
        print(settings.REDIS_PORT)
        print("************************")
        return Response({"ok": 1}, status=status.HTTP_200_OK)
