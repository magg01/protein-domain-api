from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *

@api_view(['GET','POST'])
def protein_detail(request, pk):
    try:
        protein = Protein.objects.get(pk=pk)
    except Protein.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)