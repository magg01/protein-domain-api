from django.shortcuts import render

from .models import *

# Create your views here.
def index(request):
    response_string = Protein.objects.all()[0]
    return render(request,'restAPI/index.html', {'data': response_string})