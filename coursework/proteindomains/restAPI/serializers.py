from django.db.models import fields
from django.db.models.fields.related import RelatedField
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

class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ['domain_id','domain_description']

class ProteinDomainSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()

    class Meta:
        model = ProteinDomain
        fields = ['pfam_id','description','start','stop' ]

class ProteinSerializer(serializers.ModelSerializer):
    domains = ProteinDomainSerializer(many=True, read_only=True)

    class Meta:
        model = Protein
        fields = ['protein_id','sequence','taxonomy','length','domains'] 
        depth = 1






    