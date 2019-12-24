from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import (get_key,
                          set_ttl,
                          reset_ttl,
                          set_redis_data,
                          get_redis_data,
                          string_to_dict,
                          string_splitter,
                          get_common_prefix_redis_keys)


class ValuesAPIView(APIView):
    PREFIX = "values"

    def get(self, request):
        key_args = self.request.GET.get('keys')

        if key_args:
            all_keys = string_splitter(source_str=key_args,
                                       split_by=',',
                                       prefix=self.PREFIX)          # list object -> iterable
        else:
            all_keys = get_common_prefix_redis_keys(self.PREFIX)    # generator object -> iterable

        # response = {get_key(key): get_redis_data(key=key) for key in all_keys}

        response = dict()
        for key in all_keys:
            key_data = get_redis_data(key=key)
            if key_data:
                response_key = get_key(key)
                response[response_key] = key_data

            reset_ttl(key)

        return Response(
            {
                "status": "success",
                "total": len(response),
                "data": response
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        time_to_live = 10   # seconds
        data = string_to_dict(self.request.body)

        for key in data:
            try:
                insert_key = f"{self.PREFIX}_{key}"
                set_redis_data(key=insert_key, value=data[key])
                set_ttl(key=insert_key, time_to_live=time_to_live)

            except (RedisError, Exception) as e:
                print(e)

        return Response(
            {
                "status": "success"
            },
            status=status.HTTP_201_CREATED
        )

    def patch(self, request):
        pass

