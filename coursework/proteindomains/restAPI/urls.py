from django.urls import path

from . import views
from . import api

urlpatterns = [
    # path('', views.index, name="index"),
    # path('api/protein/<int:pk>', api.ProteinDetails.as_view()),
    #path('api/protein/<str:protein_id>', api.RetrieveProteinView.as_view()),
    path('api/protein/<str:protein_id>', api.retrieveCreateProteinView),
    path('api/pfam/<str:domain_id>', api.retrievePfam),
    path('api/proteins/<str:taxa_id>', api.retrieveOrganismProteins),
    path('api/pfams/<str:taxa_id>', api.retrieveOrganismProteinDomains),
    path('api/coverage/<str:protein_id>', api.retrieveCoverage),

    path('api/proteinDomain_test/<str:protein_id>', api.retrieveProteinDomainTest),
]