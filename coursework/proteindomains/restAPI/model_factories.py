from django.test import TestCase
from django.conf import settings
from django.core.files import File
import factory
import factory.fuzzy

from .models import *

class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = factory.Sequence(lambda n: 'pfam%d' % n+str(1))
    domain_description = factory.Faker('sentence', nb_words=4, length=)
    class Meta:
        model = Pfam

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = factory.fuzzy.FuzzyInteger()
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
    start = randint(1, 50)
    stop = start + randint(1, 1000)
    description = 'a rather boring alpha helix'

    class Meta:
        model = ProteinDomain