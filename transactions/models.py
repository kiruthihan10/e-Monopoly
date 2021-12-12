from django.db import models
from django.conf import settings

class Game(models.Model):
    GameID = models.AutoField(primary_key=True)
    Banker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='banker')

    def __str__(self)->str:
        return f'GameID: {self.GameID} with Banker as {self.Banker}'

    def get_all_players(self)->list:
        transactions = Transaction.objects.filter(Game=self)
        players = []
        for transaction in transactions:
            if transaction.sender not in players:
                players.append(transaction.sender)
            if transaction.receiver not in players:
                players.append(transaction.receiver)
        return players

class Transaction(models.Model):
    TransactionID = models.AutoField(primary_key=True)
    Game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='player')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    Amount = models.IntegerField()
    Note = models.CharField(max_length=50, blank=True, null=True)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self)->str:
        return f'TransactionID: {self.TransactionID} was made by {self.receiver} to {self.sender} for {self.Amount} on {self.Date}'

# Create your models here.