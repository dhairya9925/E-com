from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import users, Cart
from core.models import Orders, Product
from mysite import settings
import os
from random import randint
from django.utils.text import slugify
import uuid
from datetime import datetime

# -------------------------------------------------------------------------------------------------------------------------

# --- Store data in sessoin ---


def get_user_from_session(request):
    try:
        user_session_id = request.COOKIES[settings.USER_SESSION_COOKIE_NAME]
        if user_session_id:
            return users.objects.get(sessionID=user_session_id)
    except users.DoesNotExist:
        return None
    except KeyError:
        return None

# def save_session(request):
#     user = get_user_from_session(request)
#     user.sessionID = request.COOKIES[']
    
def loggedin(request, user_id):

    response = HttpResponseRedirect("../")
    
    custom_session_id = uuid.uuid4()
    response.set_cookie(settings.USER_SESSION_COOKIE_NAME, custom_session_id)

    user = users.objects.get(id = user_id)
    user.sessionID = custom_session_id
    user.save()

    # request.session.cycle_key()

    return response

    # request.COOKIES[settings.USER_SESSION_COOKIE_NAME] = user_session_id
    

def authenticate(request, email, password):
    try:
        user = users.objects.get(email = email, password = password)
        if user is not None:
            return user.id
        return None
    except users.DoesNotExist:
        return None


def get_formatted_address(request):
    if request.POST is not None and len(request.POST) > 1 :
        address = {}
        for key,value in request.POST.items():
            if key != "csrfmiddlewaretoken":
                if key != "address":
                    data = {key: value}
                    address.update(data)
                else:
                    # Formatting response in request.POST["address"]
                    value = value.replace(",\r\n", ", ").replace("\r\n", ", ")
                    data = {key: value}
                    address.update(data)
        return address
        
    return None

# def access_custom_data_from_session(request):
#     # Accessing custom session data
#     user_session_id = request.session.get(settings.USER_SESSION_COOKIE_NAME, None)  # Default to None if not found
#     seller_session_id = request.session.get('seller_session_id', None)  # Default to None if not found
    
#     # You can now use these variables in your view logic
#     if user_session_id:
#         print(f"User session ID: {user_session_id}")
#     else:
#         print("User session ID not found.")
    
#     if seller_session_id:
#         print(f"Seller: {seller_session_id}")
#     else:
#         print("Seller session ID not found.")

# -------------------------------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------------------------------
# Create your views here.
def login(request):
    if request.method == "POST":
        print("\n\n---IN POST---")

        email = request.POST.get('email')
        password = request.POST.get('password')
        print("\n--- Authenticate ---")
        user = authenticate(request, email, password)
        if user is not None:
            print("\n--- Logged IN ---")
            response = loggedin(request, user)
            HttpResponseRedirect("../")
            if settings.USER_SESSION_COOKIE_NAME in request.COOKIES:
                print("session created")
            else:
                print("!! session NOT created")

            # request.user.sessionID = request.COOKIES[settings.USER_SESSION_COOKIE_NAME]
            

            print(f"Cookie Data(Logged IN) --->{request.COOKIES}")
            return response
        else:
            print("\n\n---IN ELSE---")
            return render(request, "login.html", {"message": f"Worng email or password"})
    else:
        print("\n\n---IN GET---")
        print(f"Cookie Data --->{request.COOKIES}")

        return render(request, "login.html")
        # return HttpResponseRedirect("login")


def register(request):
    if request.method == "POST":
        print("POST")
        names = users.objects.values_list("name", flat=True)
        emails = users.objects.values_list("email", flat=True)

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if name in names or email in emails:
            print("\n\n -- IF -- ")
            return render(request, "register.html", {"message": "User Already Exist! Please Login"})
        else:
            print("\n\n -- ELSE -- ")
            user = users(
                name = name, 
                email = email, 
                password = password, 
                contact = None,
                )
            user.save()
            
            # Creates the user's Cart
            cart = Cart(
                id = user.id,
                user = user,
            )
            cart.save()
            return HttpResponseRedirect("../login")
    else:
        print("\n\n -- GET -- ")
        return render(request, "register.html")


def home(request):
    # os.system("cls")
    print(f"Cookie Data(get_user_from_session) --->{request.COOKIES}")
    user = get_user_from_session(request)
    products = Product.objects.all()
    # print(f"--- IS {user} ----")
    if user is not None:
        print(f"\n\'{user}\' IS LOGGED IN {request.COOKIES["user_session_id"]}")

        # response = render(request, "home.html")
        # response.set_cookie(settings.USER_SESSION_COOKIE_NAME, request.session.session_key)


        if request.method == "POST":
            print(f"\n__ADDED_TO_CART__\n")
            currProduct = request.POST["currProduct"]
            product = Product.objects.get(id = currProduct)
            cart = Cart.objects.get(user = user)
            addStatus = {"stauts": 0}

            productList = []
            for item in cart.products:
                print(f"Item : {item}")
                for id, quantity in item.items():
                    if currProduct == id:

                        item[id] += 1
                        cart.price = (cart.price + product.price) if (cart.price is not None) else (product.price)
                        addStatus["stauts"] = 1

            if not cart.products or addStatus["stauts"] == 0:    # if cart.products is empty or addStaus is false(0)
                print(f"Add status : {addStatus['stauts']}")
                cart.products.append({
                    currProduct: 1,
                })
                cart.price += product.price
                
            # print(f"Add status : {addStatus['stauts']}")
            #     print(f"Add status : {addStatus['stauts']}")
            #     cart.products.append({
            #         "id": currProduct,
            #         "quantity": 1,
            #     })
            #     cart.price = price
            

            # Reset 
            # cart = Cart.objects.get(id = 1)
            # cart.products = []
            # cart.price = 0

            cart.save()
            

        # print(f"\n\n\n--- Products: {products} ---")
        # print(f"default session_id ---> {request.COOKIES.get("sessionid")}")
        # print(f"Cookie Data --->{request.COOKIES}")
        # print(f"custom user session_id ---> {request.session.items()}")
        return render(request, "home.html", {"user": user, "products": products})
    else:
        print("--- NOT LOGGED IN ----")
        print(f"User: {user}")
        # print(f"--- NOT LOGGED {{ user }} ----")
        return render(request, "home.html", {"products": products})


def cart(request):
    user = get_user_from_session(request)
    if user is not None:
        cart = Cart.objects.get(user = user)
        tax = (cart.price * 18)/100 if cart.price else 0
        # cart.price = tax+cart.price if tax > 0 else cart.price
        
        # productList = cart.products
        productList = [key for item in cart.products for key in item.keys()]
        print(f"productList = {productList}")
        # for i in cart.products:
        #     print(f"i = {i}")
        #     productList.append(i["id"])

        products = []
        for i in productList:
            products.append(Product.objects.get(id = i))

        # print(products)
        
        if request.method == "POST":
            # temp = request.POST["currProduct"]
            # tempP = Product.objects.get(id = temp)
            # print(f"IN POST : {tempP}")
            if "removeItem" in request.POST:
                # print(f"Delete {Product.objects.get(id = temp)} form cart")        
                currProduct = request.POST["currProduct"]
                for item in cart.products:
                    for id, quantity in item.items():
                        if currProduct == id:
                            cart.products.remove(item)
                            cart.price -= (Product.objects.get(id = currProduct).price * quantity)
                            break
                        # print(f"currProduct: {currProduct}")        
                        # print(f"item[id]: {id}")        
                        # print(f"item[currProduct]: {quantity}")        
            elif "decrement" in request.POST:
                currProduct = request.POST["currProduct"]
                for item in cart.products:
                    for id, quantity in item.items():
                        if currProduct == id:
                            if quantity > 1:
                                print("Quantity - decrement one")        
                                print(f"currProduct: {Product.objects.get(id = currProduct)}")        
                                item[id] -= 1
                            else:
                                cart.products.remove(item)
                            print(f"{Product.objects.get(id = currProduct).price} + {cart.price} Price")                    
                            cart.price -= Product.objects.get(id = currProduct).price
                            break
            elif "increment" in request.POST:
                currProduct = request.POST["currProduct"]
                for item in cart.products:
                    for id, quantity in item.items():
                        if id == currProduct:
                            print(f"currProduct: {Product.objects.get(id = currProduct)}")        
                            item[id] = quantity + 1
                            print(f"{Product.objects.get(id = currProduct).price} + {cart.price} Price")                    
                            cart.price += Product.objects.get(id = currProduct).price
                            break
            
            print(products)
            cart.save()
            return HttpResponseRedirect("../cart")
        
        context = {
            "user": user, 
            "cart": cart,
            "tax": tax,
            "products": zip(products,cart.products),
        }
        if productList == []:
            context.pop("products")
        return render(request, "cart.html", context)
    else:
        return render(request, "cart.html")


def checkout(request):
    user = get_user_from_session(request)

    if user is not None:

        if request.method == "GET":
            print(" In Get ")
            print(request.GET)

        # print(user.address)
        cart = Cart.objects.get(user = user)

        products = []
        productList = [key for item in cart.products for key in item.keys()]
        for i in productList:
            products.append(Product.objects.get(id = i))

        context = {
            "user": user,
            "cart": cart,
            "products": zip(products,cart.products),
        }

        return render(request, "checkout.html", context)

    return HttpResponseRedirect("\login")


def product_detail(request, slug, pk):
    user = get_user_from_session(request)
    if user is not None:

        product = get_object_or_404(Product, pk=pk)
        generated_slug = slugify(product.name)

        if generated_slug != slug:
            # Optionally, redirect to the correct URL
            return HttpResponseRedirect('product_detail')
        
        # relatedProducts = Product.objects.filter(category = product.category).exclude(id = product.id)
        relatedProducts = Product.objects.filter(category = product.category).exclude(id = product.id)
        if len(relatedProducts) <= 0:
            relatedProducts = None

        return render(request, 'product_detail.html', {"user": user, 'product': product, "relatedProducts": relatedProducts})
    else:
        return render(request, 'product_detail.html', {'product': product})


def profile(request):
    # Get the user from the session
    user = get_user_from_session(request)
    
    # If the user is not logged in, redirect to login
    if not user:
        return HttpResponseRedirect("../login")
    
    if request.method == "POST":
        # Handling Profile Update
        try:
            if "Profile" in request.POST:
                print(f"--- PROFILE FORM POST ---")
                
                # Update user data with form values
                user.name = request.POST.get("name", user.name)
                user.email = request.POST.get("email", user.email)
                user.password = request.POST.get("password", user.password)
                user.contact = request.POST.get("contact", user.contact)  # Only update contact if provided

                print("Changes")
                print(f"{user.name}")
                print(f"{user.email}")
                print(f"{user.password}")
                print(f"{user.contact}")
                user.save()  # Save the updated user data
                return HttpResponseRedirect("../profile")  # Redirect to the profile page after saving
                
            # Handling Account Deletion
            elif "deleteAccount" in request.POST:
                print(f"--- DELETE ACCOUNT FORM POST ---")
                password = request.POST.get("password", "")
                if password == user.password:  # Check if entered password matches user's password
                    print(f"--- User({user.name}) Deleted ---")
                    
                    # Uncomment the next line if you want to actually delete the user
                    # user.delete()  # Uncomment this line to delete the user

                    request.session.flush()  # Clear the session
                    return HttpResponseRedirect("../")  # Redirect to the homepage or login after account deletion
                else:
                    # If the passwords don't match, return an error message
                    return render(request, "profile.html", {"user": user, "message": "Password didn't match!!"})

            # print(f"-- POST data: {request.POST} --")
            return render(request, "profile.html", {"user": user})
            
        except:
            return render(request, "profile.html", {"user": user, "message2": "Duplicate record Found!!"})
    # Handling GET request or when no POST action is triggered
    return render(request, "profile.html", {"user": user})


def address(request):
    user = get_user_from_session(request)
    if user is not None:
        if request.method == "POST":
            if "edit" in request.POST:
                print("  --Edit Button Clicked")
                curr_address = get_formatted_address(request)
                for address in user.address:
                    if address["id"] == curr_address["id"]:
                        index = user.address.index(address)
                        user.address[index] = curr_address

                # address = user.address.index(curr_address)
                print(curr_address)
                # for address in user.addresses:
                    
            else:
                address = get_formatted_address(request)
                id = {"id": str("ADD-" + datetime.now().strftime("%Y%m%d-%H%M%S"))}
                address.update(id)
                print(address)
                user.address.append(address)
            print("Here")
            # print(f"Request.POST = {request.POST}")

            # delete all addresses
            # user.address = []

            user.save()
            return HttpResponseRedirect("/profile/address")
        context ={
            "user": user,
        }
        return render(request, "address.html", context)
    return HttpResponseRedirect("/login")


def logout(request):
    print("LOGGED OUT")

    response = HttpResponseRedirect("../login")   # using redirect instead of httpresonpse because
    request.session.flush()
    
    response.delete_cookie(settings.USER_SESSION_COOKIE_NAME)

    # delete all cookies
    # for cookie in request.COOKIES:
    #     response.delete_cookie(cookie)

    print(f"Cookie Data --->{request.COOKIES}")
    return response


def orderConfirmation(request):
    user = get_user_from_session(request)

    if user is not None:
        if request.method == "POST":
            print(request.POST)
            cart = Cart.objects.get(user = user)
            orderID = f"MVM-{user.id}-{datetime.now().strftime("%Y%m%d")[:8] + str(randint(10,99))}"
            print(f"orderID: {orderID}")
            print(f"Price: {request.POST}")

            order = Orders(
                orderID = orderID,
                price = request.POST['price'],
                address = request.POST['savedAddress'],
                shipment = request.POST['shippingMethod'][0].lower(),
                paymentMethod = request.POST['paymentMethod'],
                products = cart.products
            )
            order.save()
            
            # Add order to the user orderList
            # user.order.append(order.orderID)

            # user.order.remove("MVM-1-2025051949")
            # user.order.remove("MVM-1-2025051996")
            # user.save()
            
            # Remove Products from cart
            # cart.products = []
            # cart.save()

            # Delete all orders
            # order = Orders.objects.all()
            # order.delete()

            if "home" in request.POST:
                return HttpResponseRedirect("/") 
            elif "orders" in request.POST:
                return HttpResponseRedirect("/orders") 
            context = {
                "user": user,
                "order": order,
            }
            return render(request, "orderConfirmation.html", context)
        return render(request, "orderConfirmation.html")    
    return HttpResponseRedirect("/login")


def orders(request):
    user = get_user_from_session(request)
    if user is not None:
        context = {
            "user": user,
        }
        return render(request, "orders.html", context)
    return HttpResponseRedirect("/login")

# -------------------------------------------------------------------------------------------------------------------------





        # ---------------OLD WORKING CODE----------------
    #    if request.method == "POST":
    #         print(f"\n__ADDED_TO_CART__\n")
    #         currProduct = request.POST["currProduct"]
    #         product = Product.objects.get(id = currProduct)
    #         cart = Cart.objects.get(user = user)
    #         addStatus = {"stauts": 0}

    #         productList = []
    #         for item in cart.products:
    #             if currProduct == item['id']:
    #                 item["quantity"] += 1
    #                 cart.price = (cart.price + product.price) if (cart.price is not None) else (product.price)
    #                 addStatus["stauts"] = 1

    #         if not cart.products or addStatus["stauts"] == 0:    # if cart.products is empty or addStaus is false(0)
    #             print(f"Add status : {addStatus['stauts']}")
    #             cart.products.append({
    #                 "id": currProduct,
    #                 "quantity": 1,
    #             })
    #             cart.price = product.price

    #         # else:



    #         # print(f"Add status : {addStatus['stauts']}")
    #         #     print(f"Add status : {addStatus['stauts']}")
    #         #     cart.products.append({
    #         #         "id": currProduct,
    #         #         "quantity": 1,
    #         #     })
    #         #     cart.price = price
            

    #         # Reset 
    #         # cart = Cart.objects.get(id = 1)
    #         # cart.products = []
    #         # cart.price = None

    #         cart.save()
        # ---------------OLD WORKING CODE----------------
