$('#commentForm').submit(function(e){
    e.preventDefault();
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"];
    let dt = new Date()
    let time = dt.getDate() + " " + monthNames[dt.getUTCMonth()] + " " + dt.getFullYear()
    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr('method'),
        url: $(this).attr('action'),
        dataType: 'json',
        success: function(res) {
            console.log('success')
            if(res.bool == true) {
                $('#review-res').html('Review Added Success.')
                $('.hide-comment-form').hide()
                $('.add-review').hide()

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src="https://static.thenounproject.com/png/5034901-200.png" alt="" />'
                _html += '<a href="#" class="font-heading text-brand" style="margin-left: 4px;">'+res.context.user+'</a>'
                _html += '</div>'
                _html += '<div class="desc">'
                _html += '<div class="d-flex justify-content-between mb-10">'
                _html += '<div class="d-flex align-items-center">'
                _html += '<span class="font-xs text-muted">'+time+' </span>'
                _html += '</div>'

                // _html += '<div class="product-rate d-inline-block" style="margin-left: 320px;">'
                // _html += '<div class="product-rating" style="width: 100%"></div>'
                // _html += '</div>'

                for(let i = 1; i <= res.context.rating; i++) {
                    _html += '<i class="fas fa-star text-warning"></i>'
                }
                _html += '</div>'
                _html += '<p class="mb-10">'+res.context.review+' </p>'
                _html += '<a href="#" class="reply">Reply</a>'
                _html += '</div>'
                _html += '</div>'
                _html += '</div>'

                $('.comment-list').prepend(_html)
            }
        }
    })
})

$(document).ready(function() {
    $('.filter-checkbox').on('click',function(){
        let filter_object = {}

        /*
        let min_price = $('#max_price').attr('min')
        let max_price = $('#max_price').val()
        if(!max_price) {
            max_price = $('#max_price').attr('max')
        }
        */

        min_price = $('#slider-range-min').data('value')
        max_price = $('#slider-range-max').data('value')
        filter_object.min_price = min_price
        filter_object.max_price = max_price

        $('.filter-checkbox').each(function(){
            // let filter_value = $(this).val()
            let filter_key = $(this).data('filter')
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+filter_key+']:checked')).map(function(element){
                return element.value
            })
        })
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function(){
                console.log('sending data....')
            },
            success: function(res){
                if(res) {
                    $('#filtered-product').html(res.data)
                    $('div.totall-product').find('strong.text-brand').html(res.count_products)
                }
            }
        })
    })

    $('#max_price').on('blur', function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()
        if(parseFloat(current_price) < parseFloat(min_price) || current_price > parseFloat(max_price)) {
            min_price = Math.round(min_price * 100)/100
            max_price = Math.round(max_price * 100)/100
            alert('Price must between $'+ min_price +' and $'+ max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()
            return false
        }
    })

    // add to cart 
    $(document).on('click','.add-to-cart-btn', function(){
        let this_val = $(this)
        let index = this_val.data('index')

        let quantity = $('.product-quantity-'+ index).val()
        let product_title = $('.product-title-'+ index).val()
        let product_id = $('.product-id-'+ index).val()
        let product_pid = $('.product-pid-'+ index).val()
        let product_image = $('.product-image-'+ index).val()
        let product_price = $('.current-product-price-'+ index).text()
        
        console.log('quantity',quantity)
        console.log('product_title',product_title)
        console.log('product_id',product_id)
        console.log('product_pid',product_pid)
        console.log('product_image',product_image)
        console.log('product_price',product_price)
        console.log('index',index)

        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': product_id,
                'pid': product_pid,
                'title': product_title,
                'image': product_image,
                'qty': quantity,
                'price': product_price,
            },
            dataType: 'json',
            success: function(res){
                btn_name = this_val.html()
                this_val.html('✔')
                setTimeout(function(){
                    this_val.html(btn_name)
                },2000)
                console.log('Product added successfully')
                $('.cart-items-count').text(res.totalcartitems)
                if(res.cart_store) {
                    $('#cart-store').html('')
                    $('#cart-store').html(res.cart_store)
                }
            }
        })
    })

    $(document).on('click', '.delete-product', function(){
        let type = $(this).data('type')
        let product_id = $(this).data('product')
        let this_val = $(this)
        console.log('product_id',product_id)

        $.ajax({
            url: '/delete-from-cart',
            data: {
                'id': product_id
            },
            dataType: 'json',
            success: function(res) {
                // remove item from cart popup
                if(type && type == 'popup') {
                    this_val.closest('li').remove()
                }
                $('.cart-items-count').text(res.totalcartitems)
                $('#cart-list').html('')
                $('#cart-list').html(res.data)
            }
        })
    })

    $(document).on('click', '.update-product', function(){
        let type = $(this).data('type')
        let product_id = $(this).data('product')
        let this_val = $(this)
        let product_quantity = $('.product-quantity-'+product_id).val()
        console.log('product_id',product_id)

        $.ajax({
            url: '/update-cart',
            data: {
                'id': product_id,
                'qty': product_quantity,
            },
            dataType: 'json',
            success: function(res) {
                // remove item from cart popup
                if(type && type == 'popup') {
                    this_val.closest('li').remove()
                }
                $('.cart-items-count').text(res.totalcartitems)
                $('#cart-list').html('')
                $('#cart-list').html(res.data)
            }
        })
    })

    //make default address
    $(document).on('click','.make-default-address',function(){
        let id = $(this).data('address-id')
        let this_val = $(this)
        console.log('id',id)

        $.ajax({
            url: '/make-default-address',
            data: { 'id': id },
            dataType: 'json',
            success: function(res){
                console.log('Address made default....')
                if(res.success == true) {
                    $('.check').hide()
                    $('.action_btn').show()
                    
                    $('.check'+id).show()
                    $('.button'+id).hide()
                }
            }
        })
    })

    // adding to wishlist
    $(document).on('click','.add-to-wishlist',function(){
        let product_id = $(this).data('product-item')
        let this_val = $(this)
        console.log('product_id',product_id)

        $.ajax({
            url: '/add-to-wishlist',
            data: { 'id': product_id },
            dataType: 'json',
            success: function(res) {
                if(res.success == true) {
                    console.log('Added to wishlist...')
                }
            }
        })
    })

    // remove from wishlist
    $(document).on('click','.delete-wishlist-product',function(){
        let wishlist_id = $(this).data('wishlist-product')
        let this_val = $(this)
        console.log('wishlist_id',wishlist_id)

        $.ajax({
            url: '/remove-from-wishlist',
            data: { 'id': wishlist_id },
            dataType: 'json',
            success:function(res){
                console.log('Removed to wishlist...')
                $('#wishlist-list').html(res.data)
                $('#wishlistCount').html(res.wishlist_count)
            }
        })
    })

    // remove from wishlist
    $(document).on('submit','#contact-form-ajax',function(e){
        e.preventDefault()
        console.log('Submited...')
        let full_name = $('#full_name').val()
        let email = $('#email').val()
        let phone = $('#phone').val()
        let subject = $('#subject').val()
        let message = $('#message').val()

        console.log('full_name',full_name)
        console.log('email',email)
        console.log('phone',phone)
        console.log('subject',subject)
        console.log('message',message)

        $.ajax({
            url: '/ajax-contact-form',
            data: {
                'full_name': full_name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message,
            },
            dataType: 'json',
            success: function(res) {
                console.log('Sent data to server...')
                console.log('Sent data to server...')
                if(res.success == true) {
                    $('#contact-form-ajax').hide()
                    $('#message_sent').text(res.message)
                }
            }
        })

    })

    // get products by category_id
    $(document).on('click', '.cate-tab', function() {
        cid = $(this).data('cate-id')
        console.log('cid',cid)
        $.ajax({
            url: '/get-product-cate',
            data: { 'cid': cid },
            dataType: 'json',
            success: function(res) {
                console.log('res',res)
                $('#myTabContent').html(res.data)
            }
        })
    })
})


