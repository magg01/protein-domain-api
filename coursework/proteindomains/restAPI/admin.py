from django.contrib import admin

from .models import *

admin.site.register(Protein)
admin.site.register(Pfam)
admin.site.register(Organism)
admin.site.register(ProteinDomain)