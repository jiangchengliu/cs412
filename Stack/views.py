# views.py
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
import plotly.graph_objs as go
from django.contrib.auth import login

def home(request):
    return render(request, 'Stack/base.html')

#Class View to get ListView of Stocks
class StockListView(LoginRequiredMixin, ListView):
    model = Stock
    template_name = 'Stack/stock_list.html'
    paginate_by = 10
    ordering = ['name']
    
    def get_queryset(self):
        query_set = Stock.objects.all()
        query = self.request.GET.get('q')
        if query:
            query_set = query_set.filter(name__istartswith=query)
        return query_set
    

#Class View to StockDetail
class StockDetailView(LoginRequiredMixin, DetailView):
    model = Stock
    template_name = 'Stack/stock.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock = self.object 
        user_profile = self.request.user.stack_user_profile 
        
        portfolio = Portfolio.objects.filter(user=user_profile, stock=stock).first()
        context['shares_owned'] = portfolio.quantity if portfolio else 0 
        
        return context

#Class View to Profile
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'Stack/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.stack_user_profile
    
#Class View to Transactions
class TransactionsListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'Stack/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 10

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user.stack_user_profile).order_by('-created_at')

#Class View to Investing
class InvestingView(LoginRequiredMixin, ListView):
    model = Portfolio
    template_name = 'Stack/investing.html'
    context_object_name = 'portfolios'
    ordering = ['stock__name']
    paginate_by = 10
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user.stack_user_profile).order_by('stock__name')
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.request.user.stack_user_profile
        portfolios = Portfolio.objects.filter(user=profile)
     
        stocks = [item.stock.ticker for item in portfolios]
        quantities = [item.quantity for item in portfolios]
        
        investing = 0
        for portfolio in portfolios:
            investing += portfolio.stock.price * portfolio.quantity

    
        bar_chart = go.Figure(
            data=[
                go.Bar(
                    x=stocks,  
                    y=quantities,  
                    marker=dict(color='green'),  
                )
            ]
        )
        bar_chart.update_layout(
            title=dict(
                text="Stocks Owned",
                font=dict(color='lime'), 
            ),
            xaxis=dict(
                title="Stock",
                titlefont=dict(color='lime'),  
                tickfont=dict(color='lime'),  
            ),
            yaxis=dict(
                title="Shares",
                titlefont=dict(color='lime'),  
                tickfont=dict(color='lime'), 
            ),
            plot_bgcolor='black',  
            paper_bgcolor='black',  
        )

        context['bar_chart'] = bar_chart.to_html(full_html=False)
        context['watchlist_items'] = Watchlist.objects.filter(user=profile)
        context['investing'] = investing

        return context

    
#buy
def buy_stock(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST['quantity']) 
        stock = Stock.objects.get(pk=pk)
        profile = request.user.stack_user_profile  

        total = stock.price * quantity

        #check if user has enough balance
        if total > profile.balance:
            messages.error(request, 'Insufficient Funds')
            return redirect('stock_detail', pk=pk)  
        else:
            #create transaction and portfolio objects
            profile.balance -= total
            profile.save()

            transaction = Transaction(
                user=profile,
                stock=stock,
                quantity=quantity,
                price=stock.price,
                transaction_type='B' 
            ) 
            transaction.save()

            portfolio, created = Portfolio.objects.get_or_create(
                user=profile, stock=stock,
                defaults={'quantity': 0} 
            )
            portfolio.quantity += quantity
            portfolio.save()

            messages.success(request, f'Successfully purchased {quantity} shares of {stock.ticker}.')
            return redirect('stock_detail', pk=pk)

#sell
def sell_stock(request, pk):
    """
    same as buy_stock but for selling shares
    """
    if request.method == 'POST':
        try:
            quantity = request.POST.get('quantity')
            if not quantity or not quantity.isdigit():
                raise ValueError("Quantity must be a valid positive integer.")
            quantity = int(quantity)
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('stock_detail', pk=pk)

        #get stock and user profile
        stock = get_object_or_404(Stock, pk=pk)
        profile = request.user.stack_user_profile  

        total = stock.price * quantity

        #check if user has enough shares
        try:
            portfolio = Portfolio.objects.get(user=profile, stock=stock)
        except Portfolio.DoesNotExist:
            messages.error(request, "You don't own any shares of this stock.")
            return redirect('stock_detail', pk=pk)

        if portfolio.quantity < quantity:
            messages.error(request, 'Insufficient Shares')
            return redirect('stock_detail', pk=pk)

        #create transaction and portfolio objects
        profile.balance += total
        profile.save()
        portfolio.quantity -= quantity
        portfolio.save()

        Transaction.objects.create(
            user=profile,
            stock=stock,
            quantity=quantity,
            price=stock.price,
            transaction_type='S'
        )

        messages.success(request, f'Successfully sold {quantity} shares of {stock.ticker}.')
        return redirect('stock_detail', pk=pk)

#adds a certain stock to the watchlist
def add_to_watchlist(request, pk):
    #get the stock and user profile
    stock = Stock.objects.get(pk=pk)
    profile = request.user.stack_user_profile
    #create a watchlist object
    watchlist, created = Watchlist.objects.get_or_create(user=profile, stock=stock)
    if created:
        messages.success(request, f'{stock.ticker} added to watchlist.')
    else:
        messages.error(request, f'{stock.ticker} is already in your watchlist.')
    return redirect('stock_detail', pk=pk)

#Class View to CreateUserProfile
class CreateUserProfileView(CreateView):
    form_class = UserProfileForm
    template_name = 'Stack/register.html'
    
    def form_valid(self, form):
        #create a new user and use the user object to create a profile
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        login(self.request, user)
        return redirect('investing')

#Class View to UpdateProfile
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'Stack/update_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.stack_user_profile
    
     