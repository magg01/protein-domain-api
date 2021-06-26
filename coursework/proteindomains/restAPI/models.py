from django.db import models

class Protein(models.Model):
    text = models.CharField(max_length=200)

