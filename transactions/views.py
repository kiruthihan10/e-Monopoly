from django.contrib.auth import get_user_model
from .models import Transaction, Game
from .serializers import PlayerSerializer, TransactionSerializer, GameSerializer
from rest_framework import authentication, permissions, serializers, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

from datetime import datetime

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
    queryset = Transaction.objects.all()
    serializer_class = PlayerSerializer

    def retrieve(self, request):
        serializer = PlayerSerializer(data={'receiver':request.get_username()})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        
        game = Game.objects.get(pk=request.data['Game'])
        transactions = Transaction.objects.all().filter(Game=game.GameID)
        new_player = not any(
            transaction.player_on_game(request.user)
            for transaction in transactions
        )
        if not new_player:
            return Response({"error":"You are already on The game"}, status=status.HTTP_400_BAD_REQUEST)
        if game.Banker.get_username() == request.user.get_username():
            return Response({"error":"You are the Banker"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data['receiver'] = request.user.get_username()
        data['Date'] = datetime.now()
        data['Note'] = f"Game initialized for {request.user.get_username()}"
        data['Amount'] = 2000
        data['sender'] = game.Banker
        serializer = PlayerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
