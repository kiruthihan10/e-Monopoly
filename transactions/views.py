from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Transaction, Game
from .serializers import PlayerSerializer, TransactionSerializer, GameSerializer
from rest_framework import authentication, permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

User = get_user_model()


class DefaultMixin(object):
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )
    paginate_by = 25

class TransactionViewSet(DefaultMixin,viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class GameViewSet(DefaultMixin,viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def create(self, request):
        serializer = GameSerializer(data={'Banker':request.user.get_username()})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlayerViewSet(DefaultMixin,viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PlayerSerializer
# Create your views here.
