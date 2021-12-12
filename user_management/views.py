from django.contrib.auth import get_user, get_user_model
from django.shortcuts import render
from rest_framework import authentication, permissions, viewsets


from .serializers import UserSerializer
User = get_user_model()

class DefaultMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.AllowAny,
    )
    paginate_by = 25

class UserViewSet(DefaultMixin, viewsets.ModelViewSet):

    
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Create your views here.
