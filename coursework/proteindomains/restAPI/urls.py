from django.urls import path

from . import views
from . import api

urlpatterns = [  
    # endpoint 1 GET-only - protein details
    path('protein/<str:protein_id>', api.RetrieveProtein.as_view(), name='GET_protein_api'),
    # endpoint 1 PUT-only - create protein
    path('protein/', api.CreateProtein.as_view(), name='POST_protein_api'),
    # endpoint 2 - pfam details
    path('pfam/<str:domain_id>', api.RetrievePfam.as_view(), name='pfam_api'),
    # endpoint 3 - proteins in organism
    path('proteins/<str:taxa_id>', api.retrieveOrganismProteins, name='organism_protein_api'),
    # endpoint 4 - domains of proteins in organism
    path('pfams/<str:taxa_id>', api.retrieveOrganismProteinDomains, name='organism_protein_domain_api'),
    # endpoint 5 - coverage
    path('coverage/<str:protein_id>', api.retrieveCoverage, name='protein_coverage_api'),
]