from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^home/$', 'catalog.views.all_products'), (r'^my-cart/$', 'cart.views.cart'),
                       (r'^search/(?P<inputString>[A-Za-z]+)/$', 'search.views.search'),
                       (r'^add-to-cart/(?P<product_id>[\d]+)/$', 'cart.views.add_to_cart'),
                       (r'^popular-products/$', 'cart.views.popular_products'),
                       (r'^delete-cart-item/(?P<cart_item_id>[\d]+)/$', 'cart.views.delete_cart_item'),
                       (r'^checkout/$', 'checkout.views.login'), (r'^checkout/email/$', 'checkout.views.get_user_email'),
    # Examples:
    # url(r'^$', 'duqa.views.home', name='home'),
    # url(r'^duqa/', include('duqa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

'''urlpatterns += patterns('',
    url(r'^add-to-cart/(?P<product_id>[\d]+)/$', 'cart.views.add_to_cart'),
    url(r'^add-accessory-to-cart/(?P<product_id>\d*)/(?P<quantity>.*)$', "add_accessory_to_cart", name="lfs_add_accessory_to_cart"),
    url(r'^added-to-cart$', "added_to_cart", name="lfs_added_to_cart"),
    url(r'^delete-cart-item/(?P<cart_item_id>\d*)$', "delete_cart_item", name="lfs_delete_cart_item"),
    url(r'^refresh-cart$', "refresh_cart"),
    url(r'^cart$', "cart", name="lfs_cart"),
    url(r'^check-voucher-cart/$', "check_voucher", name="lfs_check_voucher_cart")
)'''

if settings.DEBUG:
    urlpatterns +=patterns('',
                           url(r'^media/(?P<path>.*)$','django.views.static.serve',{
                               'document_root':settings.MEDIA_ROOT,}),)
