from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings

redb = settings.REDIS_DB


class ValuesAPIView(APIView):
    def get(self, request):
        print("************************")
        print(settings.REDIS_HOST)
        print(settings.REDIS_PORT)
        print("************************")
        all_keys = redb.get("me")
        print(all_keys)
        print("************************")

        return Response(
            {
                "status": "ok",
                "message": "success"
            },
            status=status.HTTP_200_OK
        )
