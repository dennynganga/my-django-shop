# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Product

def all_products(request):
    products = Product.objects.all()
    return render_to_response('index.html', {'products':products}, context_instance=RequestContext(request))
    
