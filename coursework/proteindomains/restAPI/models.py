from django.db import models

class Protein(models.Model):
    protein_name = models.CharField(max_length=200)

