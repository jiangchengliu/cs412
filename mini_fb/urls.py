from django.urls import path
from .views import ShowAllProfiles

urlpatterns = [
    path("show_all_profiles", ShowAllProfiles.as_view(), name="show_all_profiles"),
]