from django.contrib.auth import authenticate, get_user, get_user_model
from django.shortcuts import get_object_or_404, render
from rest_framework import authentication, generics, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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

class UserAuthViewSet(viewsets.ReadOnlyModelViewSet):

    lookup_fields = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def validate(self, request, username = None):
        user = authenticate(username=username, password=request.query_params['password'])
        return Response({'user': user is not None})

# Create your views here.
