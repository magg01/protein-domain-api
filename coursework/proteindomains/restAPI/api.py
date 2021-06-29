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

# @api_view(['GET','POST'])
# def protein_detail(request, pk):
#     try:
#         protein = Protein.objects.get(pk=pk)
#     except Protein.DoesNotExist:
#         return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = ProteinSerializer(protein)
#         return Response(serializer.data)

class RetrieveProteinView(generics.RetrieveAPIView):
    
    queryset = Protein.objects.all()
    lookup_field = 'protein_id'
    serializer_class = ProteinSerializer

class RetrievePfam(generics.RetrieveAPIView):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    lookup_field = 'domain_id'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@api_view(['GET'])
def RetrievePfamTest(request, domain_id):
    try:
        domain = Domain.objects.get(domain_id=domain_id)
    except Domain.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DomainSerializer(domain)
        return JsonResponse(serializer.data)

@api_view(['GET','POST'])
def retrieveCreateProteinView(request, protein_id):
    if request.method == 'GET':
        try:
            protein = Protein.objects.get(protein_id=protein_id)
        except Protein.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProteinSerializer(protein)
        return JsonResponse(serializer.data)
    

@api_view(['GET'])
def retrieveProteinDomainTest(request, protein_id):
    print("reached here")
    try:
        protein = Protein.objects.get(protein_id=protein_id)
        proteinDomain = ProteinDomain.objects.filter(protein_id=protein.id)
        print(proteinDomain)
    except ProteinDomain.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProteinDomainSerializer(proteinDomain, many=True)
        return JsonResponse(serializer.data, safe=False)