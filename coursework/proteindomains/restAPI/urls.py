from django.urls import path

from . import views
from . import api

urlpatterns = [  
    # endpoint 1 GET-only
    path('protein/<str:protein_id>', api.RetrieveProtein.as_view(), name='GET_protein_api'),
    # endpoint 1 PUT-only
    path('protein/', api.CreateProtein.as_view()),
    # endpoint 2
    path('pfam/<str:domain_id>', api.RetrievePfam.as_view(), name='pfam_api'),
    # endpoint 3
    path('proteins/<str:taxa_id>', api.retrieveOrganismProteins),
    # endpoint 4
    path('pfams/<str:taxa_id>', api.retrieveOrganismProteinDomains),
    # endpoint 5
    path('coverage/<str:protein_id>', api.retrieveCoverage),
]