from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction, Game
from django.db.models import Q, query

User = get_user_model()

class GameSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField('get_players', read_only=True)
    Banker = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True,)

    # def __init__(self, banker:User = None, *args, **kwargs):
    #     if banker is None:
    #         self.Banker = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True,)
    #     else:
    #         self.Banker = banker
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = Game
        fields = ('GameID','Banker','players')

    def create(self, validated_data):
        return Game.objects.create(**validated_data)
    
    def get_players(self, obj:Game):
        transactions = Transaction.objects.filter(Game=obj)
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
    receiver = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True)
    sender = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True)
    class Meta:
        model = Transaction
        fields = 'TransactionID','Game','receiver','sender','Amount'


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def get_all_games(self, obj:User):
        games = Game.objects.all()
        return [game for game in games if obj in game.get_all_players()]