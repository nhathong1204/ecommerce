from django.shortcuts import render,get_object_or_404,redirect
from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist, Address
from userauths.models import ContactUs
from userauths.models import ContactUs, Profile
from taggit.models import Tag
from core.forms import ProductReviewForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages

#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm

from django.core import serializers

import calendar
from django.db.models import Count,Avg
from django.db.models.functions import ExtractMonth


# Create your views here.
def index(request):
    products = Product.objects.filter(product_status="published").order_by('-id')
    featured_categories = Category.objects.all().order_by('-id')
    context = {
        'products': products,
        'featured_categories': featured_categories,
    }
    return render(request, 'core/index.html',context)

def get_product_by_category(request):
    cid = request.GET.get('cid')
    if cid == all:
        category = Category.objects.get(cid=cid)
        products = Product.objects.filter(product_status="published",category=category).order_by('-id')
    else:
        products = Product.objects.filter(product_status="published").order_by('-id')

    context = render_to_string('core/async/cate-product-list.html', {
            'cid': cid,
            'products': products,
        })
    return JsonResponse({'data': context})

def product_list_view(request):
    products = Product.objects.filter(product_status="published").order_by('-id')
    context = {
        'products': products
    }
    return render(request, 'core/product-list.html',context)

def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    
    #getting review related to a product
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    
    #getting average review
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    #Product Review form
    review_form = ProductReviewForm()
    
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        
        if user_review_count > 0:
            make_review = False
    
    productRelated = Product.objects.filter(product_status="published", category=product.category).exclude(pid=pid)
    p_image = product.p_images.all()
    context = {
        'product': product,
        'p_image': p_image,
        'review_form': review_form,
        'reviews': reviews,
        'make_review': make_review ,
        'average_rating': average_rating,
        'productRelated': productRelated,
    }
    return render(request, 'core/product-detail.html',context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'core/category-list.html',context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)
    
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'core/category-product-list.html',context)

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors': vendors
    }
    return render(request, 'core/vendor-list.html',context)

def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(product_status="published", vendor=vendor)
    context = {
        'vendor': vendor,
        'products': products,
    }
    return render(request, 'core/vendor-detail.html',context)

def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by('-id')
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
        
    context = {
        'products': products,
        'tag': tag,
    }
    return render(request, 'core/tag.html', context)

def ajax_add_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST.get('review'),
        rating=request.POST.get('rating'),
    )
    
    context = {
        'user': user.username,
        'review': request.POST.get('review'),
        'rating': request.POST.get('rating'),
    }
    
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews,
        }
    )

def search_view(request):
    query = request.GET.get('q')
    category = request.GET.get('cat')
    products = Product.objects.filter(title__icontains=query,product_status="published",category=category).order_by('-date')
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'core/search.html', context)

def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')
    
    products = Product.objects.filter(product_status="published").order_by('-id').distinct()
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)
    # products = products.filter(price__lte=max_price)

    if len(categories) >0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) >0:
        products = products.filter(vendor__id__in=vendors).distinct()

    count_products = products.count()
    context = {
        'products': products,
    }

    data = render_to_string('core/async/product-list.html', context)
    return JsonResponse({'data': data, 'count_products': count_products})

def add_to_cart(request):
    cart_product = {}
    cart_product[request.GET.get('id')] = {
        'title': request.GET.get('title'),
        'qty': request.GET.get('qty'),
        'price': request.GET.get('price'),
        # 'subtotal': float(request.GET.get('price'))*int(request.GET.get('qty')),
        'image': request.GET.get('image'),
        'title': request.GET.get('title'),
        'pid': request.GET.get('pid'),
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET.get('id')) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[request.GET.get('id')]['qty'] = int(cart_product[request.GET.get('id')]['qty']) + int(cart_data[request.GET.get('id')]['qty'])
            # cart_data[request.GET.get('id')]['subtotal'] = cart_product[request.GET.get('id')]['subtotal']
            # cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
            request.session.modified = True
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product


    # add cart data to menu top
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])
                request.session['cart_data_obj'][p_id]['subtotal'] = cart_total_amount
                request.session.modified = True
    cart_store = render_to_string('core/async/cart-store.html', {'cart_total_amount': cart_total_amount,'cart_data':request.session['cart_data_obj']})
    #end add cart data to menu top
        
    context = {
        'data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_store': cart_store,
    }
        
    return JsonResponse(context)

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        context = {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        }
        return render(request, 'core/cart.html',context)
    else:
        context = {
            'cart_data': '',
            'totalcartitems': 0,
            'cart_total_amount': cart_total_amount,
        }
        return render(request, 'core/cart.html',context)
    
def delete_item_from_cart(request):
    product_id = request.GET.get('id')
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            del request.session['cart_data_obj'][product_id]
            request.session.modified = True
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('core/async/cart-list.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })
    return JsonResponse({'data': context,'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = request.GET.get('id')
    product_qty = request.GET.get('qty')
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            # cart_data = request.session['cart_data_obj']
            # cart_data[request.GET.get('id')]['qty'] = product_qty
            # cart_data.update(cart_data)
            request.session['cart_data_obj'][request.GET.get('id')]['qty'] = product_qty
            request.session['cart_data_obj'][request.GET.get('id')]['subtotal'] = int(product_qty)*float(request.session['cart_data_obj'][request.GET.get('id')]['price'])
            request.session.modified = True
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context = render_to_string('core/async/cart-list.html', {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
        })
    return JsonResponse({'data': context,'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):
    total_amount = 0
    cart_total_amount = 0
    # Checking if cart_data_obj is exists
    if 'cart_data_obj' in request.session:
        # Getting total amount for Paypal Amount
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])

        # Create Order Object
        order = CartOrder.objects.create(
            user = request.user,
            price=total_amount
        )

        # Getting total amount for the Cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

            cart_order_products = CartOrderProducts.objects.create(
                order =order,
                invoice_no='INVOICE_NO-' + str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=item['subtotal'],
            )



    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_amount,
        'item_name': 'Order-Item-No-'+ str(order.id),
        'invoice': 'INVOICE_NO-'+ str(order.id),
        # 'item_name': 'Order-Item-No-1',
        # 'invoice': 'INVOICE_NO-1',
        'currency_code': 'USD',
        'notify_url': 'https://{}{}'.format(host, reverse('core:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('core:payment-completed')),
        'cancel_return': 'http://{}{}'.format(host, reverse('core:payment-failed')),
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    
    try:
        count_active_address = Address.objects.filter(user=request.user, status=True).count()
        if(count_active_address>1):
            messages.warning(request, "There are multiple addresses, only one should be activated.")
        active_address = Address.objects.filter(user=request.user, status=True)[0]
    except:
        active_address = None

    context = {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
        'paypal_payment_button': paypal_payment_button,
        'active_address': active_address,
    }
    return render(request, 'core/checkout.html',context)

@login_required
def payment_completed_view(request):
    if request.GET.get('PayerID'):
        # from pprint import pprint
        total_amount = 0
        cart_total_amount = 0
        # Checking if cart_data_obj is exists
        if 'cart_data_obj' in request.session:
            # Getting total amount for Paypal Amount
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])

            # Create Order Object
            # order = CartOrder.objects.create(
            #     user = request.user,
            #     price=total_amount
            # )

            # Getting total amount for the Cart
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                # cart_order_products = CartOrderProducts.objects.create(
                #     order =order,
                #     invoice_no='INVOICE_NO-' + str(order.id),
                #     item=item['title'],
                #     image=item['image'],
                #     qty=item['qty'],
                #     price=item['price'],
                #     total=item['subtotal'],
                # )
        # del request.session['cart_data_obj']
            
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = {
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount,
    }
    return render(request, 'core/payment-completed.html', context)

@login_required
def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')

@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)

    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count(('id'))).values('month','count')
    month = []
    total_orders = []

    for order in orders:
        month.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])

    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, "Address Added Successfully.")
        return redirect('core:dashboard')


    context = {
        'orders_list': orders_list,
        'address': address,
        'profile': profile,
        'orders': orders,
        'month': month,
        'total_orders': total_orders,
    }
    return render(request, 'core/dashboard.html',context)
    
@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user,id=id)
    order_items = CartOrderProducts.objects.filter(order=order)
    context = {
        'order_items': order_items
    }
    return render(request, 'core/order-detail.html',context)

def make_address_default(request):
    id = request.GET.get('id')
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)

    return JsonResponse({'success': True})

@login_required
def wishlist_view(request):
    try:
        wishlist_data = wishlist.objects.all()
    except:
        wishlist_data = None
    
    context = {
        'wishlist': wishlist_data
    }

    return render(request, 'core/wishlist.html', context)

def add_to_wishlist(request):
    product_id = request.GET.get('id')
    product = Product.objects.get(id=product_id)
    
    context = {}
    wishlist_count = wishlist.objects.filter(product=product, user=request.user).count()
    
    if wishlist_count >0:
        context = {
            'success': True
        }
    else:
        new_wishlist = wishlist.objects.create(
            product=product,
            user=request.user,
        )
        context = {
            'success': True
        }
    return JsonResponse(context)

def remove_wishlist(request):
    wid = request.GET.get('id')
    wishlist_data = wishlist.objects.filter(user=request.user)

    wishlist_obj = wishlist.objects.get(id=wid)
    wishlist_obj.delete()

    context = {
        'success': True,
        'wishlist': wishlist_data
    }
    # wishlist_json = serializers.serialize('json',wishlist_data)
    data = render_to_string('core/async/wishlist-list.html',context)

    return JsonResponse({'data': data, 'wishlist_count': wishlist_data.count()})

def contact(request):
    return render(request, 'core/contact.html')

def ajax_contact_form(request):
    full_name = request.GET.get('full_name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    subject = request.GET.get('subject')
    message = request.GET.get('message')
    
    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )
    
    return JsonResponse({
        'success': True,
        'message': ' Message sent successfully.'
    })

def about_us(request):
    return render(request, 'core/about_us.html')

def purchase_guide(request):
    return render(request, 'core/purchase_guide.html')

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'core/terms_of_service.html')