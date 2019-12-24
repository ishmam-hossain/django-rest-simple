from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.conf import settings

redb = settings.REDIS_DB


class ValuesAPIView(APIView):
    def get(self, request):
        key_args = self.request.GET.get('keys')
        if key_args:
            keys_asked_for = key_args.split(',')

        all_keys = redb.scan_iter("values*")
        for k in all_keys:
            print(k)

        return Response(
            {
                "status": "ok",
                "message": "success"
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        from ast import literal_eval
        data = literal_eval(self.request.body.decode())
        insert_prefix = 'values'

        for key in data:
            try:
                redb.set(f"{insert_prefix}_{key}", data[key])
            except Exception as e:
                print(e)

        return Response(
            {
                "status": "ok",
                "message": "success",
            }
        )

    def patch(self, request):
        pass

