from django.db import models
from django.db.models.constraints import UniqueConstraint

# model class for Pfams, used to create Pfams database table
class Pfam(models.Model):
    domain_id = models.CharField(max_length=13, unique=True)
    domain_description = models.CharField(max_length=66)

# model class for Organisms, used to create Organisms database table
class Organism(models.Model):
    taxa_id = models.IntegerField(primary_key=True)
    clade = models.CharField(max_length=1)
    genus = models.CharField(max_length=127)
    species = models.CharField(max_length=127)


# model class for Proteins, used to create Proteins database table
class Protein(models.Model):
    taxonomy = models.ForeignKey(Organism, on_delete=models.PROTECT, related_name="organisms")
    protein_id = models.CharField(max_length=10, unique=True)
    sequence = models.CharField(max_length=35991, null=True, blank=True)
    length = models.IntegerField(null=True)
    # proteins have a many-to-many relationship with Pfams so this is modeled
    # through the use of a join table 'ProteinDomain'. 
    pfams = models.ManyToManyField(Pfam, through='ProteinDomain')

# model class for ProteinDomains, used to create ProteinDomains database table
class ProteinDomain(models.Model):
    protein_id = models.ForeignKey(Protein, on_delete=models.PROTECT, related_name="domains")
    pfam_id = models.ForeignKey(Pfam, on_delete=models.PROTECT)
    start = models.IntegerField()
    stop = models.IntegerField()
    description = models.CharField(max_length=147)
    class Meta:
        # ensure that a particular domain at a particular position in a particular protein
        # is unique within the table.
        constraints = [
        UniqueConstraint(fields=['protein_id', 'pfam_id', 'start', 'stop'], name='unique_domain_within_protein')
        ]
