from rest_framework import serializers
from .models import *

# class ProteinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Protein
#         fields = ['protein_name']

class ProteinDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinDomain
        fields = ['protein_id', 'domain_id', 'start', 'stop', 'description']

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id','clade','genus','species']

class ProteinSerializer(serializers.ModelSerializer):
    proteinDomain = ProteinDomainSerializer(read_only=True, many=True)

    class Meta:
        model = Protein
        fields = ['protein_id','sequence','taxonomy','length', 'domains','proteinDomain']
        depth = 3


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['domain_id','domain_description']

class ProteinDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence']




    