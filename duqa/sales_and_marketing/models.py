from django.db import models
from django.utils.translation import ugettext_lazy as _

from catalog.models import Product

class ProductSales(models.Model):
    """
    Stores total sales per product
    """
    product = models.ForeignKey(Product, verbose_name=_(u"product"))
    sales = models.IntegerField(_(u"sales"), default=0)
    
class TopSeller(models.Model):
    product = models.ForeignKey(Product, verbose_name=_(u"product"))
    position = models.PositiveSmallIntegerField(_(u"Position"), default=1)
    
    class Meta:
        ordering = ["position"]
        
    def __unicode__(self):
        return "%s (%s)" % (self.product.name, self.position)
    
class FeaturedProducts(models.Model):
    """
    Featured products are manually selected by the admin
    """
    product = models.ForeignKey(Product, verbose_name=_(u"product"))
    position = models.PositiveSmallIntegerField(_(u"Position"), default=1)
    active = models.BooleanField(_(u"Active"), default=True)
    
    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return "%s (%s)" % (self.product.name, self.position)
    