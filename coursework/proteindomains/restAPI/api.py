from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins, status, generics

from .models import *
from .serializers import *

######## GET #########
# class-based view for returning JSON at enpoint 1 - protein details
class RetrieveProtein(generics.RetrieveAPIView):
    queryset = Protein.objects.all()
    lookup_field = 'protein_id'
    serializer_class = ProteinDetailSerializer

######## POST #########
# class-based view for accepting POST request to create a new Protein record
class CreateProtein(generics.CreateAPIView):
    serializer_class = ProteinSerializer

############## endpoint 2 ###############
# class-based view for returning JSON at enpoint 2 - pfam details
class RetrievePfam(generics.RetrieveAPIView):
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer
    lookup_field = 'domain_id'


# function-based view allows only GET method
# for returning JSON at endpoint 3 - list of proteins found in a particular organism
@api_view(['GET'])
def retrieveOrganismProteins(request, taxa_id):
    if request.method == 'GET':
        try:
            organism = Organism.objects.get(taxa_id=taxa_id)
        except Organism.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        proteins = Protein.objects.filter(taxonomy=organism)

        serializer = OrganismProteinSerializer(proteins, many=True)
        return Response(serializer.data)

############## endpoint 4 ###############
# function-based view allows only GET method
# for returning JSON at endpoint 4 - list of domains for all proteins 
# found in a particular organism 
@api_view(['GET'])
def retrieveOrganismProteinDomains(request, taxa_id):
    if request.method == 'GET':
        try:
            organism = Organism.objects.get(taxa_id=taxa_id)
        except Organism.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        proteins = Protein.objects.filter(taxonomy=organism)
        domains = ProteinDomain.objects.filter(protein_id__in=proteins)

        serializer = OrganismProteinDomainSerializer(domains, many=True)
        return Response(serializer.data)

############## endpoint 5 ###############
# function-based view allows only GET method
# for returning JSON at endpoint 5 - coverage value of a particular protein
@api_view(['GET'])
def retrieveCoverage(request, protein_id):
    if request.method == 'GET':
        try:
            protein = Protein.objects.get(protein_id=protein_id)
        except Protein.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        domains = ProteinDomain.objects.filter(protein_id=protein)

        totalDomainLength = 0
        for domain in domains:
            totalDomainLength += domain.stop - domain.start

        coverage = totalDomainLength / protein.length
        return Response({"coverage": coverage})