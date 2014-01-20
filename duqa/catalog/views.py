from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Product
import json

def all_products(request):
    products = Product.objects.all()
    return render_to_response('index.html', {'products':products}, context_instance=RequestContext(request))

def all_products_mobile(request):
    return render_to_response('mobile_index.html', context_instance=RequestContext(request))

def json_products(request):
    products = Product.objects.all().values('name', 'price', 'slug', 'stock_amount', 'main_image', 'id')
    products = json.dumps(list(products))
    return HttpResponse(products, mimetype='application/json')
    
