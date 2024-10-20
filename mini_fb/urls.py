from django.urls import path
from .views import *

urlpatterns = [
    path("", ShowAllProfiles.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete/', DeleteStatusView.as_view(), name='delete_status'),
    path('status/<int:pk>/update/', UpdateStatusView.as_view(), name='update_status'),
]