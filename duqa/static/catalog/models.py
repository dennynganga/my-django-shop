import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

#app imports
from catalog.settings import CHOICES, CONTENT_CATEGORIES
from catalog.settings import CHOICES_STANDARD
from catalog.settings import CHOICES_YES
from catalog.settings import PRODUCT_TYPE_CHOICES
from catalog.settings import CONFIGURABLE_PRODUCT
from catalog.settings import STANDARD_PRODUCT
from catalog.settings import VARIANT
from catalog.settings import PRODUCT_WITH_VARIANTS
from catalog.settings import CAT_CATEGORY_PATH
from catalog.settings import CATEGORY_TEMPLATES
from catalog.settings import CONTENT_PRODUCTS
from catalog.settings import LIST
from catalog.settings import DELIVERY_TIME_UNIT_CHOICES
from catalog.settings import DELIVERY_TIME_UNIT_SINGULAR
from catalog.settings import DELIVERY_TIME_UNIT_HOURS
from catalog.settings import DELIVERY_TIME_UNIT_DAYS
from catalog.settings import DELIVERY_TIME_UNIT_WEEKS
from catalog.settings import DELIVERY_TIME_UNIT_MONTHS
from catalog.settings import PROPERTY_FIELD_CHOICES
from catalog.settings import PROPERTY_NUMBER_FIELD
from catalog.settings import PROPERTY_SELECT_FIELD
from catalog.settings import PROPERTY_TEXT_FIELD
from catalog.settings import PROPERTY_STEP_TYPE_CHOICES
from catalog.settings import PROPERTY_STEP_TYPE_AUTOMATIC
from catalog.settings import PROPERTY_STEP_TYPE_MANUAL_STEPS
from catalog.settings import PROPERTY_STEP_TYPE_FIXED_STEP
from catalog.settings import PROPERTY_VALUE_TYPE_DEFAULT
from catalog.settings import PROPERTY_VALUE_TYPE_DISPLAY
from catalog.settings import PROPERTY_VALUE_TYPE_VARIANT
from catalog.settings import PRODUCT_TEMPLATES
from catalog.settings import QUANTITY_FIELD_TYPES
from catalog.settings import QUANTITY_FIELD_INTEGER
from catalog.settings import QUANTITY_FIELD_DECIMAL_1
from catalog.settings import THUMBNAIL_SIZES
from catalog.settings import VARIANTS_DISPLAY_TYPE_CHOICES
from catalog.settings import CATEGORY_VARIANT_CHEAPEST_PRICE
from catalog.settings import CATEGORY_VARIANT_CHEAPEST_BASE_PRICE
from catalog.settings import CATEGORY_VARIANT_CHEAPEST_PRICES
from catalog.settings import CATEGORY_VARIANT_DEFAULT

def get_unique_id_str():
    return str(uuid.uuid4())

class Category(models.Model):
    name = models.CharField(_(u"Name"), max_length=50)
    products = models.ManyToManyField("Product", verbose_name=_(u"Products"), blank=True, related_name="categories")
    short_description = models.TextField(_(u"Short description"), blank=True)
    description = models.TextField(_(u"Description"), blank=True)
    categoryid = models.CharField(max_length=50, editable=False, unique=True, default=get_unique_id_str)
    
    meta_title = models.CharField(_(u"Meta title"), max_length=100, default="<name>")
    meta_keywords = models.TextField(_(u"Meta keywords"), blank=True)
    meta_description = models.TextField(_(u"Meta description"), blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)

class Product(models.Model):
    name = models.CharField(_(u"Name"), help_text=_(u"The name of the product."), max_length=80, blank=True)
    slug = models.SlugField(_(u"Slug"), help_text=_(u"The unique last part of the Product's URL."), unique=True, max_length=80)
    sku = models.CharField(_(u"SKU"), help_text=_(u"Your unique article number of the product."), blank=True, max_length=30)
    price = models.FloatField(_(u"Price"), default=0.0)
    main_image = models.ImageField(_(u"Image"), upload_to="product-images")
    #images = generic.GenericRelation("Image", verbose_name=_(u"Images"), object_id_field="content_id", content_type_field="content_type")
    short_description = models.TextField(_(u"Short description"), blank=True)
    description = models.TextField(_(u"Description"), blank=True)
    productid = models.CharField(max_length=50, editable=False, unique=True, default=get_unique_id_str)
    
    meta_title = models.CharField(_(u"Meta title"), blank=True, default="<name>", max_length=80)
    meta_keywords = models.TextField(_(u"Meta keywords"), blank=True)
    meta_description = models.TextField(_(u"Meta description"), blank=True)
    
    related_products = models.ManyToManyField("self", verbose_name=_(u"Related products"), blank=True, null=True,
        symmetrical=False, related_name="reverse_related_products")
    
    accessories = models.ManyToManyField("Product", verbose_name=_(u"Acessories"), blank=True, null=True,
        symmetrical=False, through="ProductAccessories",
        related_name="reverse_accessories")
    
    for_sale = models.BooleanField(_(u"For sale"), default=False)
    active = models.BooleanField(_(u"Active"), default=False)
    creation_date = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    
    #Stocks
    stock_amount = models.IntegerField(_(u"Stock amount"), default=0)
    deliverable = models.BooleanField(_(u"Deliverable"), default=True)
    
    class Meta:
        db_table = 'products'
        ordering = ('name', )
        
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)
    
    def decrease_stock_amount(self, amount):
        self.stock_amount -= amount
        self.save
        
'''class Image(models.Model):
    title = models.CharField(_(u"Title"), blank=True, max_length=100)
    image = models.ImageField(upload_to='product-images')
    class Meta:
        db_table = 'images'
    
    def __unicode__(self):
        return self.title'''
        
class ProductAccessories(models.Model):
    product = models.ForeignKey("Product", verbose_name=_(u"Product"), related_name="productaccessories_product")
    accessory = models.ForeignKey("Product", verbose_name=_(u"Accessory"), related_name="productaccessories_accessory")
    position = models.IntegerField(_(u"Position"), default=999)
    quantity = models.FloatField(_(u"Quantity"), default=1)
    
    class Meta:
        ordering = ("position", )
        verbose_name_plural = "Product accessories"
        db_table = 'ProductAccessories'

    def __unicode__(self):
        return "%s -> %s" % (self.product.name, self.accessory.name)

    def get_price(self, request):
        """
        Returns the total price of the accessory based on the product price and
        the quantity in which the accessory is offered.
        """
        return self.accessory.get_price(request) * self.quantity
    
class DeliveryTime(models.Model):
    """
    Selectable delivery times.

    **Attributes:**

    min
        The minimal lasting of the delivery date.

    max
        The maximal lasting of the delivery date.

    unit
        The unit of the delivery date, e.g. days, months.

    description
        A short description for internal uses.

    """
    min = models.FloatField(_(u"Min"))
    max = models.FloatField(_(u"Max"))
    unit = models.PositiveSmallIntegerField(_(u"Unit"), choices=DELIVERY_TIME_UNIT_CHOICES, default=DELIVERY_TIME_UNIT_DAYS)
    description = models.TextField(_(u"Description"), blank=True)

    class Meta:
        ordering = ("min", )
        db_table = 'deliverytimes'

    def __unicode__(self):
        return self.round().as_string()

    def __gt__(self, other):
        if self.max > other.max:
            return True
        return False

    def __add__(self, other):
        """
        Adds to delivery times.
        """
        # If necessary we transform both delivery times to the same base (hours)
        if self.unit != other.unit:
            a = self.as_hours()
            b = other.as_hours()
            unit_new = DELIVERY_TIME_UNIT_HOURS
        else:
            a = self
            b = other
            unit_new = self.unit

        # Now we can add both
        min_new = a.min + b.min
        max_new = a.max + b.max
        unit_new = a.unit

        return DeliveryTime(min=min_new, max=max_new, unit=unit_new)

    @property
    def name(self):
        """
        Returns the name of the delivery time
        """
        return self.round().as_string()

    def subtract_days(self, days):
        """
        Substract the given days from delivery time's min and max. Takes the
        unit into account.
        """
        if self.unit == DELIVERY_TIME_UNIT_HOURS:
            max_new = self.max - (24 * days)
            min_new = self.min - (24 * days)
        elif self.unit == DELIVERY_TIME_UNIT_DAYS:
            max_new = self.max - days
            min_new = self.min - days
        elif self.unit == DELIVERY_TIME_UNIT_WEEKS:
            max_new = self.max - (days / 7.0)
            min_new = self.min - (days / 7.0)
        elif self.unit == DELIVERY_TIME_UNIT_MONTHS:
            max_new = self.max - (days / 30.0)
            min_new = self.min - (days / 30.0)

        if min_new < 0:
            min_new = 0
        if max_new < 0:
            max_new = 0

        return DeliveryTime(min=min_new, max=max_new, unit=self.unit)

    def as_hours(self):
        """
        Returns the delivery time in hours.
        """
        if self.unit == DELIVERY_TIME_UNIT_HOURS:
            max = self.max
            min = self.min
        elif self.unit == DELIVERY_TIME_UNIT_DAYS:
            max = self.max * 24
            min = self.min * 24
        elif self.unit == DELIVERY_TIME_UNIT_WEEKS:
            max = self.max * 24 * 7
            min = self.min * 24 * 7
        elif self.unit == DELIVERY_TIME_UNIT_MONTHS:
            max = self.max * 24 * 30
            min = self.min * 24 * 30

        return DeliveryTime(min=min, max=max, unit=DELIVERY_TIME_UNIT_HOURS)

    def as_days(self):
        """
        Returns the delivery time in days.
        """
        if self.unit == DELIVERY_TIME_UNIT_HOURS:
            min = self.min / 24
            max = self.max / 24
        elif self.unit == DELIVERY_TIME_UNIT_DAYS:
            max = self.max
            min = self.min
        elif self.unit == DELIVERY_TIME_UNIT_WEEKS:
            max = self.max * 7
            min = self.min * 7
        elif self.unit == DELIVERY_TIME_UNIT_MONTHS:
            max = self.max * 30
            min = self.min * 30

        return DeliveryTime(min=min, max=max, unit=DELIVERY_TIME_UNIT_DAYS)

    def as_weeks(self):
        """
        Returns the delivery time in weeks.
        """
        if self.unit == DELIVERY_TIME_UNIT_HOURS:
            min = self.min / (24 * 7)
            max = self.max / (24 * 7)
        elif self.unit == DELIVERY_TIME_UNIT_DAYS:
            max = self.max / 7
            min = self.min / 7
        elif self.unit == DELIVERY_TIME_UNIT_WEEKS:
            max = self.max
            min = self.min
        elif self.unit == DELIVERY_TIME_UNIT_MONTHS:
            max = self.max * 4
            min = self.min * 4

        return DeliveryTime(min=min, max=max, unit=DELIVERY_TIME_UNIT_WEEKS)

    def as_months(self):
        """
        Returns the delivery time in months.
        """
        if self.unit == DELIVERY_TIME_UNIT_HOURS:
            min = self.min / (24 * 30)
            max = self.max / (24 * 30)
        elif self.unit == DELIVERY_TIME_UNIT_DAYS:
            max = self.max / 30
            min = self.min / 30
        elif self.unit == DELIVERY_TIME_UNIT_WEEKS:
            max = self.max / 4
            min = self.min / 4
        elif self.unit == DELIVERY_TIME_UNIT_MONTHS:
            max = self.max
            min = self.min

        return DeliveryTime(min=min, max=max, unit=DELIVERY_TIME_UNIT_MONTHS)

    def as_reasonable_unit(self):
        """
        Returns the delivery time as reasonable unit based on the max hours.

        This is used to show the delivery time to the shop customer.
        """
        delivery_time = self.as_hours()

        if delivery_time.max > 1440:               # > 2 months
            return delivery_time.as_months()
        elif delivery_time.max > 168:              # > 1 week
            return delivery_time.as_weeks()
        elif delivery_time.max > 48:               # > 2 days
            return delivery_time.as_days()
        else:
            return delivery_time

    def as_string(self):
        """
        Returns the delivery time as string.
        """
        if self.min == 0:
            self.min = self.max

        if self.min == self.max:
            if self.min == 1:
                unit = DELIVERY_TIME_UNIT_SINGULAR[self.unit]
            else:
                unit = self.get_unit_display()

            return "%s %s" % (self.min, unit)
        else:
            return "%s-%s %s" % (self.min, self.max, self.get_unit_display())

    def round(self):
        """
        Rounds the min/max of the delivery time to an integer and returns a new
        DeliveryTime object.
        """
        min = int("%.0f" % (self.min + 0.001))
        max = int("%.0f" % (self.max + 0.001))

        return DeliveryTime(min=min, max=max, unit=self.unit)
    
    