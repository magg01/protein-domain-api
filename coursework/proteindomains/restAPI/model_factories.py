import factory
from django.test import TestCase
from django.conf import settings
from django.core.files import File

from .models import *

class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = 'PF20012'
    domain_description = 'This is a good description of a pfam'

    class Meta:
        model = Pfam

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = 123451
    clade = 'H'
    genus = "Danaus"
    species = "plexippus"

    class Meta:
        model = Organism

class ProteinFactory(factory.django.DjangoModelFactory):
    taxonomy = factory.SubFactory(PfamFactory)
    protein_id = "ProteinXX"
    sequence = "YEJENALDJ"
    length = 9

class ProteinDomainFactory(factory.django.DjangoModelFactory):
    protein_id = factory.RelatedFactory(ProteinFactory)
    pfam_id = factory.RelatedFactory(OrganismFactory)
    start = 24
    stop = 220
    description = 'a rather boring alpha helix'

    class Meta:
        model = ProteinDomain