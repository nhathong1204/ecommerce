from django.contrib import admin
from core.models import Product, Category, Vendor, CartOrder, CartOrderProducts, ProductImages, ProductReview, wishlist, Address

# Register your models here.
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user','pid','title','product_description','product_image','category','vendor','price','featured','product_status']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']
    
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']
    
class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user','price','paid_status','order_date','product_status']
    
class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item','order_img','qty','price','total']
    
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']
    
class wishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']
    
class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address','status']
    list_display = ['user','address','status']
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(CartOrder,CartOrderAdmin)
admin.site.register(CartOrderProducts,CartOrderProductsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(wishlist,wishlistAdmin)
admin.site.register(Address,AddressAdmin)