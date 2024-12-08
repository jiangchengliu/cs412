from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.home, name='home'),
    path('investing/', views.InvestingView.as_view(), name='investing'),
    path('stocks/', views.StockListView.as_view(), name='stock_list'),
    path('stock/<int:pk>/', views.StockDetailView.as_view(), name='stock_detail'),
    path('stock/buy/<int:pk>/', views.buy_stock, name='buy_stock'),
    path('stock/sell/<int:pk>/', views.sell_stock, name='sell_stock'),
    path('stock/add_to_watchlist/<int:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('transactions/', views.TransactionsListView.as_view(), name='transaction_list'),
    path('register/', views.CreateUserProfileView.as_view(), name='stack_register'),
    path('login/', LoginView.as_view(template_name='Stack/login.html'), name='stack_login'),
     path('logout/', LogoutView.as_view(next_page='/Stack/'), name='stack_logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
]