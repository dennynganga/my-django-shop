from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from catalog.models import Product
class Cart(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    session = models.CharField(_(u"Session"), blank=True, null=True, max_length=100)
    creation_date = models.DateTimeField(_(u"Creation Date"), auto_now_add=True)
    modification_date = models.DateTimeField(_(u"Modification Date"), auto_now=True, auto_now_add=True)

    def __unicode__(self):
        #return u"%s, %s" % (self.user, self.session)
        return u"%s" % (self.session)
    
    def add(self, product, amount=1):
        """
        Adds passed product to the cart.
        Returns the newly created cart item.
        """
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.amount += float(amount)
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=self, product=product, amount=amount)
        cart_item.save()
        return cart_item
    
    def get_number_of_items(self):
        amount = 0
        for each in self.get_items():
            amount += each.amount
        return amount
    
    def get_items(self): #Returns items in the cart
        cart_items = CartItem.objects.filter(cart=self)
        return cart_items
    
    def get_total_price(self, request, total=False):
        """
        Returns the total gross price of all items.
        """
        price = 0
        for item in self.get_items():
            price += item.get_price_gross(request)
        return price
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name=_(u"Cart"))
    product = models.ForeignKey(Product, verbose_name=_(u"Product"))
    amount = models.IntegerField(_(u"Quantity"), blank=True, null=True)
    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    modification_date = models.DateTimeField(_(u"Modification date"), auto_now=True, auto_now_add=True)

    class Meta:
        ordering = ['id']
        
    def get_price(self, product_id, amount):
        pass
        
    def get_price_gross(self, request):
        '''
        Returns the total price of the cart item, which is just the multiplication
        of the product's price and the amount of the product within in the cart.
        '''
        return (self.product.price * self.amount)
        
    def get_price_net(self, request):
        """
        Returns the total price of the cart item, which is just the multiplication
        of the product's price and the amount of the product within in the cart.
        """
        #return self.get_price_gross(request) - self.get_tax(request)
    
    def __unicode__(self):
        return u"Product: %(product)s, Quantity: %(amount)f, Cart: %(cart)s" % {'product': self.product,
                                                                                'amount': self.amount,
                                                                                'cart': self.cart}
