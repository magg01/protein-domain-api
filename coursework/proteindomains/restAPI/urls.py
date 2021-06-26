from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('', views.index, name="index"),
    path('api/protein/<int:pk>', api.ProteinDetails.as_view()),
]