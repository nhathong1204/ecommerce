from django.urls import path,include
from . import views

app_name = 'core'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    
    
    path('get-product-cate/', views.get_product_by_category, name='get-product-cate'),
    
    # Products page
    path('products/', views.product_list_view, name='product-list'),
    path('product/<pid>/', views.product_detail_view, name='product-detail'),
    
    # Categories page
    path('category/', views.category_list_view, name='category-list'),
    path('category/<cid>/', views.category_product_list_view, name='category-product-list'),
    
    # Vendor page
    path('vendors/', views.vendor_list_view, name='vendor-list'),
    path('vendors/<vid>/', views.vendor_detail_view, name='vendor-detail'),
    
    # Tags page
    path('products/tag/<slug:tag_slug>/', views.tag_list, name='tags'),
    
    # add reviews
    path('ajax_add_review/<int:pid>/', views.ajax_add_review, name='ajax-add-review'),
    
    # search
    path('search/', views.search_view, name='search'),
    
    # filter
    path('filter-products/', views.filter_product, name='filter-product'),
    
    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    # cart page
    path('cart/', views.cart_view, name='cart'),
    
    # delete item from cart
    path('delete-from-cart/', views.delete_item_from_cart, name='delete-from-cart'),
    
    # update cart
    path('update-cart/', views.update_cart, name='update-cart'),
    
    # checkout page
    path('checkout/', views.checkout_view, name='checkout'),
    
    # paypal
    path('paypal/', include('paypal.standard.ipn.urls')),
    
    # paypal success page
    path('payment-completed/', views.payment_completed_view, name='payment-completed'),
    
    # paypal failed page
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),
    
    # customer dashboard page
    path('dashboard/', views.customer_dashboard, name='dashboard'),
    
    # order detail page
    path('dashboard/order/<int:id>', views.order_detail, name='order-detail'),
    
    # making address default
    path('make-default-address/', views.make_address_default, name='make-default-address'),
    
    # wishlist page
    path('wishlist/', views.wishlist_view, name='wishlist'),
    
    # adding to wishlist
    path('add-to-wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    
    # remove from wishlist
    path('remove-from-wishlist/', views.remove_wishlist, name='remove-from-wishlist'),
    
    
    path('contact/', views.contact, name='contact'),
    path('ajax-contact-form/', views.ajax_contact_form, name='ajax-contact-form'),
    path('about-us/', views.about_us, name='about-us'),
    path('purchase-guide/', views.purchase_guide, name='purchase-guide'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
]
