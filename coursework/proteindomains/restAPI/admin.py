from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Protein)
admin.site.register(Domain)
admin.site.register(Organism)
admin.site.register(ProteinDomain)