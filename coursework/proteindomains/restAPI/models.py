from django.db import models
from django.db.models.fields.related import ForeignKey

#this was a test - remove all mentions
#class Protein(models.Model):
#    protein_name = models.CharField(max_length=200)

class Organism(models.Model):
    taxa_id = models.IntegerField(primary_key=True)
    clade = models.CharField(max_length=1)
    genus = models.CharField(max_length=127)
    species = models.CharField(max_length=127)

class Domain(models.Model):
    domain_id = models.CharField(max_length=13)
    domain_description = models.CharField(max_length=66)

class Protein(models.Model):
    taxonomy = models.ForeignKey(Organism, on_delete=models.PROTECT)
    protein_id = models.CharField(max_length=10)
    sequence = models.CharField(max_length=35991)
    length = models.IntegerField()
    domains = models.ManyToManyField(Domain, through='ProteinDomain')

class ProteinDomain(models.Model):
    protein_id = models.ForeignKey(Protein, on_delete=models.PROTECT)
    domain_id = models.ForeignKey(Domain, on_delete=models.PROTECT)
    start = models.IntegerField()
    stop = models.IntegerField()
    description = models.CharField(max_length=147)
