from rest_framework import serializers
from .models import *

# class ProteinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Protein
#         fields = ['protein_name']

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id','clade','genus','species']