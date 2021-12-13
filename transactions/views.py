from django.contrib.auth import get_user_model
from .models import Transaction, Game
from .serializers import PlayerSerializer, TransactionSerializer, GameSerializer
from rest_framework import authentication, permissions, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

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
    lookup_field = 'game'
    lookup_url_kwarg = 'game'
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.all().filter(Q(sender=self.request.user) | Q(receiver=self.request.user))

    def create(self, request)->Response:
        data = request.data.copy()
        data['sender'] = request.user.get_username()
        print(data['sender'],data['receiver'])
        if data['sender'] == data['receiver']:
            return Response({"error": "Sender and receiver cannot be the same"}, status=status.HTTP_400_BAD_REQUEST)
        game = Game.objects.get(pk=request.data['Game'])
        print(game)
        transactions = Transaction.objects.all().filter(Game=game.GameID)
        new_player = not any(
            transaction.player_on_game(request.user)
            for transaction in transactions
        )
        if new_player and game.Banker != request.user:
            return Response({"error": "You are not on the game"}, status=status.HTTP_400_BAD_REQUEST)
        elif game.Banker != request.user and game.get_players_balance()[request.user] < int(request.data['Amount']):
            return Response({"error": "You don't have enough money"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, game=None):
        game = Game.objects.get(pk=game)
        players = game.get_players_balance()
        str_players = []
        for player in players:
            Banker = player == game.Banker
            str_players.append({'player':str(player),'balance':players[player],'Banker':Banker})
        # str_players = {str(player): players[player] for player in players}
        return Response(str_players)

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

    def list(self, request):
        transactions = Transaction.objects.all().filter(Q(receiver=request.user) | Q(sender=request.user))
        my_games = []
        my_games_IDs = []
        for transaction in transactions:
            if transaction.Game not in my_games_IDs:
                my_games.append({'GameID':transaction.Game.GameID,'Title':str(transaction.Game),'last_player':transaction.Date})
                my_games_IDs.append(transaction.Game)
            else:
                for game in my_games:
                    if game['GameID'] == transaction.Game.GameID:
                        game['last_player'] = transaction.Date
        games = Game.objects.all().filter(Banker=request.user)
        for game in games:
            if game not in my_games_IDs:
                my_games.append({'GameID':game.GameID,'Title':str(game),'last_player':None})
        return Response(my_games)

    def retrieve(self, request, *args, **kwargs):
        return self.list(request)       

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
        data['Note'] = f"Game initialized for {request.user.get_username()}"
        data['Amount'] = 2000
        data['sender'] = game.Banker
        serializer = PlayerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionHistoryViewSet(DefaultMixin,viewsets.ReadOnlyModelViewSet):
    lookup_field = 'game'
    lookup_url_kwarg = 'game'
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request, game=None):
        base_logic = Q(receiver=request.user) | Q(sender=request.user)
        logic = base_logic & Q(Game=game) if game is not None else base_logic
        transactions = Transaction.objects.all().filter(logic)
        serialized_transactions = [
            TransactionSerializer(transaction).data for transaction in transactions
        ]

        return Response(serialized_transactions)

    def retrieve(self, request, game=None):
        return self.list(request, game)

# Create your views here.
