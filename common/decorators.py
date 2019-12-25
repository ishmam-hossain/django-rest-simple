from rest_framework.response import Response
from rest_framework import status


def valid_request(f):
    def decorated_func(self, request, *args, **kwargs):
        if self.request.data:
            return f(self, request, *args, **kwargs)
        else:
            return Response({
                "status": "fail",
                "message": "json not provided"
            }, status=status.HTTP_400_BAD_REQUEST)

    return decorated_func
