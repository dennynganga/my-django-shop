from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count
import json

from models import Cart, CartItem

from catalog.models import Product
import cart_utils

def cart(request):
    '''
    Main view of the cart with the actual content
    '''
    cart = cart_utils.get_or_create_cart(request)
    cart_items = []
    for cart_item in cart.get_items():
        product = cart_item.product.name
        stock_amount = cart_item.product.stock_amount
        product_id = cart_item.product.id
        cart_item_id = cart_item.id
        quantity = cart_item.amount
        cart_items.append({
                           #"obj": cart_item,
                           "quantity": quantity,
                           "stock_amount": stock_amount,
                           "product": product,
                           "product_id": product_id,
                           "cart_item_id": cart_item_id,
                           "product_price_gross": "{:,}".format(cart_item.get_price_gross(request)),
                           })
    total_price = "{:,}".format(cart.get_total_price(request))
    return HttpResponse(json.dumps({'cart_items':cart_items, 'total':total_price}), mimetype = 'application/json')

def add_to_cart(request, product_id):
    if request.is_ajax():
        product_to_add = Product.objects.get(pk=product_id)
        product = Product.objects.filter(pk=product_id).values('name', ('price'), 'slug', 'stock_amount', 'id')
        cart = cart_utils.get_or_create_cart(request)
        quantityOptions = product[0].get('stock_amount')
        quantity = 1
        cart_item = cart.add(product_to_add, quantity)
        json_products = json.dumps(list(product), quantityOptions)
        #cart_items = [cart_item]
        #amount = json.dumps({"product":cart_item.amount})
        #print ('got %s' %(cart))
        return HttpResponse(json_products, mimetype='application/json')
    else:
        return HttpResponse('')
    
def popular_products(request):
    if cart_utils.get_cart(request) is None:
        pass
    else:
        cart = cart_utils.get_cart(request)
    popular_products = CartItem.objects.distinct().exclude(cart=cart.id).annotate(c=Count('product'))[:3]
    return render_to_response('personalised_catalog.html', {'popular_products':popular_products})
    
def cart_item_total(request, item_id, quantity):
    cart = Cart.objects.get(session = request.session.session_key)
    cart_item = CartItem.objects.get(pk = item_id)
    if request.is_ajax():
        cart_item.amount = quantity
        cart_item.save()
        total_price = "{:,}".format(cart_item.get_price_gross(request))
        cart_total = "{:,}".format(cart.get_total_price(request))
        total_price = json.dumps({'total_price':total_price, 'cart_total':cart_total})
        return HttpResponse(total_price)
    return HttpResponse('')  
        
def delete_cart_item(request, cart_item_id):
    CartItem.objects.get(pk=cart_item_id).delete()
    return HttpResponse('')
    
