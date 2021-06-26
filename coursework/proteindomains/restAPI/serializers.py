from rest_framework import serializers
from .models import *

class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['protein_name']