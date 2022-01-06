from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction, Game

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

    def create(self, validated_data)->Game:
        return Game.objects.create(**validated_data)
    
    def get_players(self, obj:Game) -> list:
        transactions = Transaction.objects.filter(Game=obj)
        players = {}
        for transaction in transactions:
            if str(transaction.receiver) not in players:
                players[str(transaction.receiver)] = transaction.Amount
            else:
                players[str(transaction.receiver)] += transaction.Amount
            if str(transaction.sender) not in players:
                players[str(transaction.sender)] = -transaction.Amount
            else:
                players[str(transaction.sender)] -= transaction.Amount
        players[str(obj.Banker)] += 20580
        return [{'name':key,'value':value} for key, value in players.items()]

class TransactionSerializer(serializers.ModelSerializer):
    receiver = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True)
    sender = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True)
    Game = serializers.SlugRelatedField(slug_field='GameID',queryset=Game.objects.all(),required=True)

    class Meta:
        model = Transaction
        fields = 'Game','receiver','sender','Amount'
    
class PlayerSerializer(serializers.ModelSerializer):
    receiver = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True)
    Game = serializers.SlugRelatedField(slug_field='GameID',queryset=Game.objects.all(),required=True)
    Note = serializers.CharField(write_only=True)
    Amount = serializers.IntegerField(write_only=True)
    Date  = serializers.DateTimeField(read_only=True)
    sender = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD,queryset=User.objects.all(),required=True,write_only=True)
    class Meta:
        model = Transaction
        fields = ('TransactionID','receiver','Game','Note','Amount','sender','Date')