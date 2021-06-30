from django.db.models import fields
from django.db.models.fields.related import RelatedField
from rest_framework import serializers
from .models import *

# Protein serializer used to serialize/deserialize protein objects on all fields
class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = '__all__'

# Pfam serializer used to serialize Pfam objects 
# (omitting auto generated 'id' field)
class PfamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pfam
        fields = ['domain_id','domain_description']

# ProteinDomain serializer used to serialize ProteinDomain objects 
# (omitting 'protein_id' field)
class ProteinDomainSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()
    class Meta:
        model = ProteinDomain
        fields = ['pfam_id','description','start','stop']

# Protein serializer used to serialize all details about a particular protein
# Used for endpoint 1 GET method.
class ProteinDetailSerializer(serializers.ModelSerializer):
    domains = ProteinDomainSerializer(many=True, read_only=True)
    class Meta:
        model = Protein
        fields = ['protein_id','sequence','taxonomy','length','domains'] 
        depth = 1

# Protein serializer used in endpoint 3 for displaying proteins
# found in a particular Organism
class OrganismProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = ['id','protein_id']

# ProteinDomain serializer used in endpoint 4 to display all domains 
# in all proteins for a given Organism
class OrganismProteinDomainSerializer(serializers.ModelSerializer):
    pfam_id = PfamSerializer()
    class Meta:
        model = ProteinDomain
        fields = ['id', 'pfam_id']
    