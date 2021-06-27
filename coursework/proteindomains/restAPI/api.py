from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins
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

class OrganismDetails(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    
    queryset = Organism.objects.all()
    serializer_class = OrganismSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)