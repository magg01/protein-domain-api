from django.contrib import admin

from .models import *

# register the models with the admin site so we can view the database
# using the built in Django admin site
admin.site.register(Protein)
admin.site.register(Pfam)
admin.site.register(Organism)
admin.site.register(ProteinDomain)