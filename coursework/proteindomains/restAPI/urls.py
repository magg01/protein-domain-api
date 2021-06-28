from django.urls import path

from . import views
from . import api

urlpatterns = [
    # path('', views.index, name="index"),
    # path('api/protein/<int:pk>', api.ProteinDetails.as_view()),
    path('api/protein/<str:protein_id>', api.RetrieveProteinView.as_view()),
    path('api/pfam/<str:domain_id>', api.RetrievePfam.as_view()),
    path('api/pfam_test/<str:domain_id>', api.RetrievePfamTest),
    path('api/protein_test/<str:protein_id>', api.retrieveCreateProteinView),
]