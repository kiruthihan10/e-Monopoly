from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Transaction, Game
from .serializers import TransactionSerializer, GameSerializer
from rest_framework import authentication, permissions, viewsets

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

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    
# Create your views here.
