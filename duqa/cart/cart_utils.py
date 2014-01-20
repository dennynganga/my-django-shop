from django.core.exceptions import ObjectDoesNotExist

from models import Cart, CartItem

def get_or_create_cart(request):
    """
    Returns the cart of the current user. If no cart exists yet it creates a
    new one first.
    """
    cart = get_cart(request)
    if cart is None:
        cart = create_cart(request)
    return cart


def create_cart(request):
    """
    Creates a cart for the current session and/or user.
    """
    if not request.session.exists(request.session.session_key):
        request.session.create()
    cart = Cart(session=request.session.session_key)
    if request.user.is_authenticated():
        cart.user = request.user

    cart.save()
    return cart

def get_cart(request):
    """
    Returns the cart of the current shop customer. if the customer has no cart
    yet it returns None.
    """
    
    session_key = request.session.session_key
    user = request.user
    '''cart = Cart.objects.get(session=session_key)
    return cart'''

    if user.is_authenticated():
        try:
            cart = Cart.objects.get(user=user)
            return cart
        except ObjectDoesNotExist:
            return None
    else:
        try:
            cart = Cart.objects.get(session=session_key)
            return cart
        except ObjectDoesNotExist:
            return None
        