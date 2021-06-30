from random import randint

import factory
import factory.fuzzy

from .models import *

class PfamFactory(factory.django.DjangoModelFactory):
    domain_id = factory.fuzzy.FuzzyText(length=randint(1,13))
    domain_description = factory.Faker('sentence', nb_words=4)
    class Meta:
        model = Pfam

class OrganismFactory(factory.django.DjangoModelFactory):
    taxa_id = factory.fuzzy.FuzzyInteger(0)
    clade = factory.fuzzy.FuzzyText(length=1)
    genus = factory.Faker('word')
    species = factory.Faker('word')

    class Meta:
        model = Organism

class ProteinFactory(factory.django.DjangoModelFactory):
    taxonomy = factory.SubFactory(PfamFactory)
    protein_id = factory.fuzzy.FuzzyText(length=randint(1,10))
    sequence = factory.fuzzy.FuzzyText(length=randint(1,35991))
    length = factory.fuzzy.FuzzyInteger(35991)

class ProteinDomainFactory(factory.django.DjangoModelFactory):
    protein_id = factory.RelatedFactory(ProteinFactory)
    pfam_id = factory.RelatedFactory(OrganismFactory)
    start = factory.fuzzy.FuzzyInteger(0,20000)
    stop = factory.fuzzy.FuzzyInteger(20000, 35991)
    description = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = ProteinDomain