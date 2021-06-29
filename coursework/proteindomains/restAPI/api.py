from django.db.models import query
from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.serializers import Serializer
from .models import *
from .serializers import *

############## endpoint 1 ###############
######## GET #########
# class-based view
class RetrieveProtein(generics.RetrieveAPIView):
    queryset = Protein.objects.all()
    lookup_field = 'protein_id'
    serializer_class = ProteinDetailSerializer

    #return bare Json - not the view
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

# function-based view
# @api_view(['GET'])
# def retrieveCreateProteinView(request, protein_id):
#     if request.method == 'GET':
#         try:
#             protein = Protein.objects.get(protein_id=protein_id)
#         except Protein.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = ProteinDetailSerializer(protein)
#         return JsonResponse(serializer.data)
#     elif request.method == 'POST':
#         JsonResponse({'test': 'ok'})

######## POST #########
# class-based view
class CreateProtein(generics.CreateAPIView):
    serializer_class = ProteinSerializer

############## endpoint 2 ###############

# class-based view
class RetrievePfam(generics.RetrieveAPIView):
    queryset = Pfam.objects.all()
    serializer_class = PfamSerializer
    lookup_field = 'domain_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Serializer = self.get_serializer(instance)
        return JsonResponse(Serializer.data)

# function-based view
# @api_view(['GET'])
# def retrievePfam(request, domain_id):
#     if request.method == 'GET':
#         try:
#             pfam = Pfam.objects.get(domain_id=domain_id)
#         except Pfam.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = PfamSerializer(pfam)
#         return JsonResponse(serializer.data)

############## endpoint 3 ###############

# function-based view
@api_view(['GET'])
def retrieveOrganismProteins(request, taxa_id):
    if request.method == 'GET':
        try:
            organism = Organism.objects.get(taxa_id=taxa_id)
        except Organism.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        proteins = Protein.objects.filter(taxonomy=organism)

        serializer = OrganismProteinSerializer(proteins, many=True)
        return JsonResponse(serializer.data, safe=False)

############## endpoint 4 ###############

# function-based view
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
        return JsonResponse(serializer.data, safe=False)

############## endpoint 5 ###############

# function-based view
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
        return JsonResponse({"coverage": coverage})


#class RetrievePfam(generics.RetrieveAPIView):
#     queryset = Pfam.objects.all()
#     serializer_class = PfamSerializer
#     lookup_field = 'domain_id'

#     def get(self, request, *args, **kwargs):
#         return super().get(request, *args, **kwargs)

# class RetrieveProteinView(generics.mixins.CreateAPIView, generics.RetrieveAPIView):
#     queryset = Protein.objects.all()
#     lookup_field = 'protein_id'
#     serializer_class = ProteinSerializer
    

# @api_view(['GET'])
# def retrieveProteinDomainTest(request, protein_id):
#     try:
#         protein = Protein.objects.get(protein_id=protein_id)
#         proteinDomain = ProteinDomain.objects.filter(protein_id=protein.id)
#         print(proteinDomain)
#     except ProteinDomain.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = ProteinDomainSerializer(proteinDomain, many=True)
#         return JsonResponse(serializer.data, safe=False)