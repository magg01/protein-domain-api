from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import *
from .serializers import *

@csrf_exempt
def protein_detail(request, pk):
    try:
        protein = Protein.objects.get(pk=pk)
    except Protein.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = ProteinSerializer(protein)
        return JsonResponse(serializer.data)