from django.urls import path
from .views import ShowAllVoters , ShowVoter, GraphsView

urlpatterns = [
    path('', ShowAllVoters.as_view(), name='voters'),
    path('voter/<int:pk>', ShowVoter.as_view(), name='voter'),
    path('graphs/', GraphsView.as_view(), name='graphs'),
]