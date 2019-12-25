from redis.exceptions import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from common.utils import (get_key,
                          set_ttl,
                          reset_ttl,
                          set_redis_data,
                          get_redis_data,
                          key_in_redis,
                          string_splitter,
                          get_common_prefix_redis_keys)


class ValuesAPIView(APIView):
    PREFIX = "values"
    TTL = 10

    @staticmethod
    def get_response_and_reset_ttl(all_keys):
        _response = dict()

        for key in all_keys:
            key_data = get_redis_data(key)
            if key_data:
                _response[get_key(key)] = key_data

            # TODO: add support for keys not found

            reset_ttl(key)

        return _response

    def get(self, request):
        key_args = self.request.GET.get('keys')

        if key_args:
            all_keys = string_splitter(source_str=key_args,
                                       split_by=',',
                                       prefix=self.PREFIX)          # list object -> iterable
        else:
            all_keys = get_common_prefix_redis_keys(self.PREFIX)    # generator object -> iterable

        response = self.get_response_and_reset_ttl(all_keys)

        return Response(
            {
                "status": "success",
                "total": len(response),
                "data": response
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        data = self.request.data
        errors = []

        for key in data:
            try:
                insert_key = f"{self.PREFIX}:{key}"
                set_redis_data(key=insert_key, value=data[key])
                set_ttl(key=insert_key, time_to_live=self.TTL)

            except (RedisError, Exception) as e:
                errors.append(f"{key} -> {e}")

        return Response(
            {
                "status": "success",
                "errors": errors if errors else None
            },
            status=status.HTTP_201_CREATED
        )

    def patch(self, request):
        data = self.request.data
        missing_keys = []
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
                missing_keys.append(key)

        return Response(
            {
                "status": "success",
                "missing_keys": missing_keys,
                "errors": errors if errors else None
            },
            status=status.HTTP_200_OK
        )

# TODO: add approriate message
