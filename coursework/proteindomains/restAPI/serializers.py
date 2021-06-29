from django.db.models import fields
from rest_framework import serializers
from .models import *

# class ProteinSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Protein
#         fields = ['protein_name']

class ProteinDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinDomain
        fields = ['domain_id', 'description', 'start', 'stop' ]
        depth = 2

class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ['taxa_id','clade','genus','species']

class DomainSerializer(serializers.ModelSerializer):
    domain_id = ProteinDomainSerializer(many=True, read_only=True)

    class Meta:
        model = Domain
        fields = ['domain_id','domain_description']

class ProteinSerializer(serializers.ModelSerializer):
    domains = ProteinDomainSerializer(many=True, read_only=True)
    
    class Meta:
        model = Protein
        fields = ['protein_id','sequence','taxonomy','length', 'domains']
        depth = 2




    