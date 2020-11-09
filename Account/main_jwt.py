from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
#!serialization section
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        # token['fav_color'] = user.fav_color
        if user.studentAuth.all():
            token["type"] = "Student"
            token["acc_id"] = user.studentAuth.all()[0].regno
        elif user.teacherAuth.all():
            token["type"] = "Admin"
            token["acc_id"] = user.teacherAuth.all()[0].id
        return token

#! View Section
class ObtainTokenPairWithDataView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

#!url Section
urlpatterns = [
    path('token/obtain/', ObtainTokenPairWithDataView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]