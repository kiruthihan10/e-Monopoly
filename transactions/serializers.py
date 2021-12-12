from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction, Game
from django.db.models import Q

class GameSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField('get_players')
    class Meta:
        model = Game
        fields = ('__all__','players')
    
    def get_players(self, obj:Game):
        transactions = Transaction.objects.filter(game=obj)
        players = []
        for transaction in transactions:
            if transaction.receiver not in players:
                players.append({transaction.player:transaction.Amount})
            else:
                players[transaction.player] += transaction.Amount
            if transaction.sender not in players:
                players.append({transaction.player:-transaction.Amount})
            else:
                players[transaction.player] -= transaction.Amount
        return players

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

User = get_user_model()
class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def get_all_games(self, obj:User):
        games = Game.objects.all()
        return [game for game in games if obj in game.get_all_players()]