import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response

from catalog.models import Product

def search(request, inputString):
    if request.is_ajax():
        search_results = json.dumps(list(Product.objects.filter(Q(name__istartswith=inputString)).values('name','main_image','short_description','slug')))
        return HttpResponse(search_results, mimetype = 'application/json')
    #return HttpResponse('')
    #return render_to_response('search_results.html',{'search_results':search_results})
