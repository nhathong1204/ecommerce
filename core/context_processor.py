from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist, Address
from django.db.models import Min,Max
from taggit.models import Tag
from django.contrib import messages

def default(request):
    vendors = Vendor.objects.all()
    categories = Category.objects.all()
    products = Product.objects.filter(product_status="published")
    tags = Tag.objects.all()
    
    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
        
    min_max_price = Product.objects.aggregate(Min('price'),Max('price'))

    try:
        wishlist_data = wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "You need to login before accessing your wishlist")
        wishlist_data = 0

    #get cart
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        cart_data = request.session['cart_data_obj']
    else:
        cart_data = ''
    
    return {
        'categories': categories,
        'products': products,
        'address': address,
        'vendors': vendors,
        'tags': tags,
        'min_max_price': min_max_price,
        'cart_data': cart_data,
        'cart_total_amount': cart_total_amount,
        'wishlist': wishlist_data,
    }