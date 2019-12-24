from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import (get_key,
                          get_redis_data,
                          string_splitter, )

redb = settings.REDIS_DB


class ValuesAPIView(APIView):
    PREFIX = "values"

    def get(self, request):
        key_args = self.request.GET.get('keys')

        if key_args:
            all_keys = string_splitter(
                source_str=key_args,
                split_by=',',
                prefix=self.PREFIX
            )   # list -> iterable
        else:
            all_keys = redb.scan_iter(f"{self.PREFIX}*")    # generator object -> iterable

        response = {get_key(key): get_redis_data(redb=redb, key=key) for key in all_keys}

        return Response(
            {
                "status": "success",
                "total": len(response),
                "data": response
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

