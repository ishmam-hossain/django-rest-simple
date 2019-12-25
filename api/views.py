from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.decorators import valid_request
from common.utils import (set_ttl,
                          set_redis_data,
                          key_in_redis,
                          string_splitter,
                          get_common_prefix_redis_keys,
                          get_response_and_reset_ttl)


class ValuesAPIView(APIView):
    PREFIX = "values"
    TTL = 5 * 60    # 5 minutes TTL

    def get(self, request):
        key_args = self.request.GET.get('keys')

        if key_args:
            all_keys = string_splitter(source_str=key_args,
                                       split_by=',',
                                       prefix=self.PREFIX)          # list object -> iterable
        else:
            all_keys = get_common_prefix_redis_keys(self.PREFIX)    # generator object -> iterable

        response, not_found = get_response_and_reset_ttl(all_keys)

        return Response(
            {
                "status": "success",
                "total": len(response),
                "data": response,
                "not_found": not_found
            },
            status=status.HTTP_200_OK
        )

    @valid_request
    def post(self, request):
        data = self.request.data
        errors = []

        for key in data:
            insert_key = f"{self.PREFIX}:{key}"

            try:
                set_redis_data(key=insert_key, value=data[key])
                set_ttl(key=insert_key, time_to_live=self.TTL)

            except (RedisError, Exception) as e:
                errors.append(f"{key} -> {e}")

        return Response(
            {
                "status": "success",
                "errors": errors
            },
            status=status.HTTP_201_CREATED
        )

    @valid_request
    def patch(self, request):
        data = self.request.data
        not_found = []
        errors = []

        for key in data:
            update_key = f"{self.PREFIX}:{key}"

            if key_in_redis(update_key):
                try:
                    set_redis_data(key=update_key, value=data[key])
                    set_ttl(key=update_key, time_to_live=self.TTL)

                except (RedisError, Exception) as e:
                    errors.append(e)
            else:
                not_found.append(key)

        return Response(
            {
                "status": "success",
                "not_found": not_found,
                "errors": errors
            },
            status=status.HTTP_200_OK
        )

# TODO: add appropriate message
