from django.urls import path
from .views import (
AuthenticateStudent,
ResultStore,
)

urlpatterns = [
    path("auth/", AuthenticateStudent.as_view(), name="auth"),
    path("result/", ResultStore.as_view(), name="result"),
]

