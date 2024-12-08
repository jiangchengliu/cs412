from django.db import models
from django.contrib.auth.models import User


# Create your models here.
#Stock Investment App

class Profile(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    image_url = models.URLField(null=True, blank=True, default='https://cdn.creazilla.com/cliparts/3153276/user-clipart-xl.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stack_user_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500000.00)
    
    def __str__(self):
        return self.user.username

    def get_balance(self):
        return self.balance


class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.ticker  

class Portfolio(models.Model):  
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_portfolios')  
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='portfolio_stocks') 
    quantity = models.IntegerField()

    class Meta:
        unique_together = ['user', 'stock']

    def __str__(self):
        return f"{self.user.user.username} - {self.stock.ticker}"

class Transaction(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_transaction') 
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_transactions')  
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=1, choices=[('B', 'Buy'), ('S', 'Sell')], default='B')

    def __str__(self):
        return f"{self.user} - {self.stock.ticker}"
    
    def get_total(self):
        return self.quantity * self.price
    

class Watchlist(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_watchlists')  
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='watchlist_stocks') 

    def __str__(self):
        return f"{self.user} is watching {self.stock.ticker}"



    
