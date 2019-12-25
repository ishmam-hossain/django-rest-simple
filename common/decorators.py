from rest_framework.response import Response
from rest_framework import status
from json import JSONDecodeError


def valid_request(f):
    def decorated_func(self, request, *args, **kwargs):
        try:
            _ = self.request.data
        except (JSONDecodeError, Exception) as e:
            return Response({
                "status": "fail",
                "message": "invalid json"
            }, status=status.HTTP_400_BAD_REQUEST)

        if not self.request.data:
            return Response({
                "status": "fail",
                "message": "json not provided"
            }, status=status.HTTP_400_BAD_REQUEST)

        return f(self, request, *args, **kwargs)

    return decorated_func
