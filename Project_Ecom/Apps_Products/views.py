from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import math


# Start reusable algorithm or functions
# increased/decreased quantity
def update_quantity(quantity, c_id):
    cart_item = CartItem.objects.get(id=c_id)
    quantitys = cart_item.quantity
    user = cart_item.user
    option = cart_item.option
    product = cart_item.product
    if quantity == "plus":
        quantitys += 1
    elif quantity == "max":
        quantitys = 10
    elif quantity == "min":
        quantitys = 1
    else:
        quantitys -= 1
    CartItem(id=c_id, quantity=quantitys, user=user, option=option, product=product).save()
    return quantitys


# shipping cost calculation algorithm
def shipping_cost(user):
    ships = CartItem.objects.filter(Q(user=user) & Q(option=True))
    shipping = 0.00
    if len(ships) >= 1:
        for ship in ships:
            if ship.product.sale_price < 1000:
                if ship.quantity > 1:
                    shipping += 30 * ship.quantity
                else:
                    shipping += 35 * ship.quantity
            else:
                if ship.quantity > 1:
                    shipping += ship.product.sale_price / 100 * 3 * ship.quantity
                else:
                    shipping += ship.product.sale_price / 100 * 3.5 * ship.quantity
        if shipping < 45:
            shipping = 45
    else:
        shipping = 0.00
    return shipping


# sub total calculation algorithm
def sub_total(user):
    totals = CartItem.objects.filter(Q(user=user) & Q(option=True))
    total = 0.00
    if totals is not None:
        for t in totals:
            price = t.product.sale_price
            total += price * t.quantity
    else:
        total = 0.00
    return total


# authentication algorithm
def authentication(request, email, password):
    user = auth.authenticate(username=email, password=password)
    if user is not None:
        auth.login(request, user)
    else:
        return render(request, 'Apps_Products/login.html')


# check box algorithm
def cart_item_data_save(c_id, product, user, option):
    quantity = CartItem.objects.get(id=c_id)
    quantity = quantity.quantity
    itm = CartItem(id=c_id, quantity=quantity, user=user, option=option, product=product)
    itm.save()


# cupon discount algorith
def cupon_discount(last, user):
    total = sub_total(user)
    amount = 0.00
    discounts = Discount.objects.filter(Q(user=user) & Q(cupon_code=last))
    if total >= last.min_spend:
        if last.type == "Fixed" or last.amount >= 100:
            amount = last.amount
        else:
            amount = math.ceil((total / 100) * last.amount)

        if discounts.exists():
            discounted = discounts[0]
            if discounted.used:
                amount = 0.00
            else:
                Discount(pk=discounted.id, user=user, used=False, cupon_code=last, discount=amount).save()
        else:
            Discount(user=user, used=False, cupon_code=last, discount=amount).save()
    return amount


def discount_amount(user):
    if Discount.objects.filter(Q(user=user) & Q(used=False)).exists():
        amount = Discount.objects.get(user=user)
        amount = amount.discount
    else:
        amount = 0.00
    return amount


def clear_discount(user):
    discount = Discount.objects.filter(Q(user=user) & Q(used=False))
    if discount.exists():
        clear = True
        for i in discount:
            i.delete()
    else:
        clear = False
    return clear


# ____________________end reusable algorithm or functions_____________________


# check box functionality
def check_item(request):
    if request.method == 'POST':
        # current user
        user = request.user
        # remove the cupon discount
        clear_discount(user)
        # get the items id
        c_id = int(request.POST['c_id'])
        # get object of the car item
        x = CartItem.objects.get(id=c_id)
        product = x.product
        option = x.option
        # discounted amount
        discount = discount_amount(user)
        # check the item is selected or not
        if option:
            option = False
            cart_item_data_save(c_id, product, user, option)
        else:
            option = True
            cart_item_data_save(c_id, product, user, option)
        # item total price counter
        item_total = x.quantity * x.product.sale_price
        # sub total counter
        total = sub_total(user)
        # shipping cost counter
        shipping = shipping_cost(user)
        # grand total or final total counter
        grand_total = total + shipping - discount
        # sending data to frontend
        item_data = {
            'c_id': c_id,
            'option': option,
            'item_total': item_total,
            'sub_total': total,
            'grand_total': grand_total,
            'shipping': shipping,
        }
        return JsonResponse(item_data)
    else:
        return redirect("/addcart")


# home page functionality
def home(request):
    # getting all products
    products = Product.objects.all()
    # separate featured products
    featured_products = [p for p in products[::-1]]
    products = featured_products[:10]
    # geting categories
    cat = Category.objects.all()
    category = []
    for p in products:
        x = p.cat
        for c in cat:
            if c == x:
                if x not in category:
                    category.append(x)
    return render(request, "home.html", {'products': products, 'category': category})
# end homepage


# search engine function
def search(request):
    if request.method == 'POST':
        # getting user input
        key = request.POST['search_input'].split()
        # getting info from all products and filter it accordingly
        data = Product.objects.all()
        match1 = []
        match2 = []
        match3 = []

        for product in data:
            for k in key:
                if len(k) >= 3:
                    p_n = product.name.split()
                    p_d = product.description.split()
                    for p in p_n:
                        q1 = k.lower()
                        q3 = p.lower()
                        if q1 == q3:
                            if product not in match1:
                                match1.append(product)
                        elif q1[0:3] == q3[0:3]:
                            if product not in match1:
                                match1.append(product)
                        elif q1[-4:] == q3[-4:]:
                            if product not in match2:
                                match2.append(product)
                    for p in p_d:
                        q1 = k.lower()
                        q3 = p.lower()
                        if q1 == q3:
                            if product not in match2:
                                match2.append(product)
                        elif q1[0:3] == q3[0:3]:
                            if product not in match3:
                                match3.append(product)
                        elif q1[-4:] == q3[-4:]:
                            if product not in match3:
                                match3.append(product)
        match = []
        for m1 in match1:
            match.append(m1)
        for m2 in match2:
            if m2 not in match:
                match.append(m2)
        for m3 in match3:
            if m3 not in match:
                match.append(m3)
        return render(request, "Apps_Products/search.html", {'match': match})
# end search engine


# Product details page function
def product_details(request, product_id):
    # getting specefic product
    product = Product.objects.get(id=product_id)
    # getting image gallery for the same product
    galery_image = Gallery.objects.filter(product=product)
    gallery = []
    for x in galery_image:
        gallery.append(x)
    return render(request, 'Apps_Products/product-detail.html', {'product': product, 'galery': gallery})
# end product details


# user login and register
def user_registration(request):
    if request.method == "POST":
        # getting first name from user
        first_name = request.POST['First_Name']
        # getting last name from user
        last_name = request.POST['Last_Name']
        # getting first name from user
        email = request.POST['Email']
        # getting first password from user
        password = request.POST['Password']
        # getting first confirm password from user
        confirm_password = request.POST['Confirm_Password']
        # password varification
        if len(password) >= 6 and password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.warning(request, "user name or email taken")
                return redirect('user_registration')
            else:
                user = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                authentication(request, email, password)
                messages.success(request, "user created")
                return redirect('/')
        else:
            messages.warning(request, "Password not matching or password length is less then 6 character")
            return redirect('user_registration')
    else:
        return render(request, 'Apps_Products/register.html')


# user login
def user_login(request):
    if request.method == "POST":
        # get email or username input from user
        email = request.POST['Email']
        # get password input from user
        password = request.POST['Password']
        # checking the authenticate condition
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            authentication(request, email, password)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
        else:
            messages.warning(request, "Email or password not matching")
            return redirect('/')
    else:
        return render(request, 'Apps_Products/login.html')


# user logout
def user_logout(request):
    auth.logout(request)
    return redirect("/")


# Add to cart functionality
@login_required(login_url='user_login')
def addcart(request):
    # get the current user
    user = request.user
    if request.method == 'POST':
        # clear cupon discount
        clear_discount(user)
        # get product id
        c_id = int(request.POST['c_id'])
        # get the specific product
        product = Product.objects.get(id=c_id)
        # check the product is already available in user cart or not
        item = CartItem.objects.filter(Q(user=user) & Q(product=product)).exists()
        option = True
        if item:
            option = False
        else:
            itm = CartItem(product=product, user=user, option=option)
            itm.save()
        item_data = {
            'option': option,
        }
        return JsonResponse(item_data)
    else:
        # get the cupon discount amount
        discount = discount_amount(user)
        # get the all cart items from the current user
        cart_item = CartItem.objects.filter(user=user)
        product_cart = []
        for i in cart_item[::-1]:
            product_cart.append(i)
        # total cost counter
        total = sub_total(user)
        # shipping cost counter
        shipping = shipping_cost(user)
        # grand total counter
        grand_total = total + shipping - discount
        # print(CartItem.is_expired())
        return render(request, 'Apps_Products/cart.html', {'cart_item': product_cart, 'total': total, 'discount': discount, 'shipping': shipping, 'grand_total': grand_total})


# Add to cart functionality
def remove_cart(request):
    if request.method == "POST":
        # get the current user
        user = request.user
        # clear cupon discount
        clear_discount(user)
        # get the cart item id
        c_id = int(request.POST['c_id'])
        # cross check the item and remove it
        rem_itm = CartItem.objects.get(Q(id=c_id) & Q(user=user))
        rem_itm.delete()
        # discount counter
        discount = discount_amount(user)
        # sub total counter
        total = sub_total(user)
        # shipping cost counter
        shipping = shipping_cost(user)
        # grand total counter
        grand_total = total + shipping - discount
        # send data to frontend
        status = {
            'value': "success",
            'sub_total': total,
            'grand_total': grand_total,
            'shipping': shipping,

            }
        return JsonResponse(status)
    else:
        return redirect("addcart")


# increased quantity
def btn_plus(request):
    # get current user
    user = request.user
    # checking request methode with if condition
    if request.method == "POST":
        # cupon discount clear_discount
        clear_discount(user)
        # get input from user
        c_id = int(request.POST['c_id'])
        # getting cart items by id
        cart_item = CartItem.objects.get(id=c_id)
        # get the sale price of the specific item
        sale_price = cart_item.product.sale_price
        # checking condition if the cart is empty or not
        if cart_item is not None:
            if cart_item.quantity < 10:
                quantity = "plus"
                quantity = update_quantity(quantity, c_id)
            else:
                # maximum quantity
                quantity = "max"
                quantity = update_quantity(quantity, c_id)
            # cupondiscount counter
            discount = discount_amount(user)
            # sub total counter
            total = sub_total(user)
            # shipping cost counter
            shipping = shipping_cost(user)
            # grand total cost counter
            grand_total = total + shipping - discount
            # item total cost counter
            item_total = quantity * sale_price
            # send data with json responce
            plus_data = {
                'quantity': quantity,
                'item_total': item_total,
                'sub_total': total,
                'grand_total': grand_total,
                'shipping': shipping,
                }
            return JsonResponse(plus_data)
    else:
        return redirect("/addcart")


# decreased quantity
def btn_minus(request):
    # get the current user
    user = request.user
    # check the requset methode with condition
    if request.method == "POST":
        # clear cupon discount
        clear_discount(user)
        # user input
        c_id = int(request.POST['c_id'])
        # match cart item
        cart_item = CartItem.objects.get(id=c_id)
        sale_price = cart_item.product.sale_price
        # cart item value check if it is null or not
        if cart_item is not None:
            if cart_item.quantity > 1:
                # decreasing quantity
                quantity = "minus"
                quantity = update_quantity(quantity, c_id)
            else:
                # Minimum quantity
                quantity = "min"
                quantity = update_quantity(quantity, c_id)
            # cupon discount counter
            discount = discount_amount(user)
            # sub total counter
            total = sub_total(user)
            # shipping cost counter
            shipping = shipping_cost(user)
            # grand total cost counter
            grand_total = total + shipping - discount
            # item total cost counter
            item_total = quantity * sale_price
            # send data with json responce
            minus_data = {
                'quantity': quantity,
                'item_total': item_total,
                'sub_total': total,
                'grand_total': grand_total,
                'shipping': shipping,
            }
            return JsonResponse(minus_data)
    else:
        return redirect("/addcart")


# cupon discount
def cupon(request):
    # check the request methode
    if request.method == "POST":
        # get the current user
        user = request.user
        # user input
        code = request.POST['values']
        # check cupon validation
        if Cupon.objects.filter(code=code).exists():
            cupon = Cupon.objects.filter(code=code)
            *rest, last = cupon
            amount = cupon_discount(last, user)
            if amount <= 0:
                messages.info(request, "You are not eligible or you already use this cupon code")
        else:
            messages.warning(request, "This cupon code is not valid")
            return redirect("/addcart")

    return redirect("/addcart")
