from django.urls import path
from .views import ValuesAPIView

urlpatterns = [
    path('values/', ValuesAPIView.as_view()),
]
