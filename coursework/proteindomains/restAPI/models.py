from django.db import models
from django.db.models import constraints
from django.db.models.constraints import UniqueConstraint

#this was a test - remove all mentions
#class Protein(models.Model):
#    protein_name = models.CharField(max_length=200)

class Organism(models.Model):
    taxa_id = models.IntegerField(primary_key=True)
    clade = models.CharField(max_length=1)
    genus = models.CharField(max_length=127)
    species = models.CharField(max_length=127)

class Pfam(models.Model):
    domain_id = models.CharField(max_length=13, unique=True)
    domain_description = models.CharField(max_length=66)

class Protein(models.Model):
    taxonomy = models.ForeignKey(Organism, on_delete=models.PROTECT)
    protein_id = models.CharField(max_length=10, unique=True)
    sequence = models.CharField(max_length=35991, null=True)
    length = models.IntegerField()
    pfams = models.ManyToManyField(Pfam, through='ProteinDomain')

class ProteinDomain(models.Model):
    protein_id = models.ForeignKey(Protein, on_delete=models.PROTECT, related_name="domains")
    pfam_id = models.ForeignKey(Pfam, on_delete=models.PROTECT)
    start = models.IntegerField()
    stop = models.IntegerField()
    description = models.CharField(max_length=147)
    class Meta:
        constraints = [
        UniqueConstraint(fields=['protein_id', 'pfam_id', 'start', 'stop'], name='unique_domain_within_protein')
        ]
