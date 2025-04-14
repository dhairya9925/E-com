from django.shortcuts import render
from django.http import HttpResponseRedirect
import json
import hashlib
from core.models import countryCode, Product, Orders
from .models import Seller
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
from mysite import settings
import uuid
from .forms import UpdateSeller

# -------------------------------------------------------------------------------------------------------------------------

# --- Store data in sessoin ---
def get_seller_from_session(request):
    try:
        seller = Seller.objects.get(sessionID = request.COOKIES[settings.SELLER_SESSION_COOKIE_NAME])
        if seller is not None:
            return seller
    except Seller.DoesNotExist:
        return None


def loggedin(request, seller_id):
    
    response = HttpResponseRedirect("../seller")
    
    custom_session_id = uuid.uuid4()
    response.set_cookie(settings.SELLER_SESSION_COOKIE_NAME, custom_session_id)

    seller = Seller.objects.get(id = seller_id)
    seller.sessionID = custom_session_id
    seller.save()

    return response


def authenticate(request, email, password):
    try:
        seller = Seller.objects.get(email = email, password = password)
        if seller is not None:
            return seller.id
        return None
    except Seller.DoesNotExist:
        return None


# # Logic functions

# def insert():
#     with open('/workspaces/Document_Updater/djangotrial/seller/countryCode.json', "r+") as file:
#         data = json.load(file)
#         for val in data:
#             country = val["name"]
#             dialCodes = val["dialCodes"]
#             image = val["image"]
#             if len(dialCodes) > 1:
#                 for dialCode in dialCodes:
#                     sReg = countryCode(country = country, dialCode = dialCode,image = image)
#                     sReg.save()
#                     print(f"country = {country}, dialCode = {dialCode},image = {image}")
#                 print("--- More than 1 dialCode ---")
#             else:
#                 sReg = countryCode(country = country, dialCode = dialCodes[0],image = image)
#                 sReg.save()
#                 print(f"country = {country},\ndialCode = {dialCodes[0]},\nimage = {image}\n\n")
#     return 0

# -------------------------------------------------------------------------------------------------------------------------


# --- Create your views here --- 

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        seller_id = authenticate(request, email, password)

        if seller_id is not None:
            response = loggedin(request, seller_id)
            
            return response
        else:
            return render(request, "Slogin.html", {"message": f"Worng email or password"})
    else:
        return render(request, "Slogin.html")


def register(request):
    countryCodes = countryCode.objects.all().values()
    first = countryCodes[0]
    if request.method == "POST":

        
        # password = password.encode()
        # password = hashlib.sha256(password)

        seller = {
            "name" : request.POST["name"],
            "email" : request.POST["email"],
            "dialCode" : request.POST["dialCode"],
            "contact" : request.POST["email"],
            "password" : request.POST["password"],
        }
        request.session["seller"] = seller
        print(f"=== {request.session["seller"]} ===")
        if request.session["seller"] is not None:
            return HttpResponseRedirect("gstin")
        # print(type(dialCode))
        # print(type(contact))

        # country = countryCode[1]
        # print(f"-- REQUESTED \"POST\"{} METHOD --")
        # register = Seller(username = user["name"], email = user["email"], password = user["password"], contact = user["contact"])
        # register.save()
        # return render(request, "dashboard.html", {"name": name})
        return render(request, "Sregister.html")
    else:
        print("GET")
    return render(request, "Sregister.html", {'countryCodes': countryCodes, 'first': first})


def gstin(request):
    print(f" --- {request.session.get("seller")} --- ")
    if request.method == "POST":

        seller_data = request.session.get("seller")
        print(f" --- {seller_data} --- ")

        if seller_data is not None:
            seller = Seller(
                name = seller_data["name"],
                email = seller_data["email"],
                dialCode = seller_data["dialCode"],
                contact = seller_data["contact"],
                password = seller_data["password"],
                address = request.POST["address"],
                city = request.POST["city"],
                district = request.POST["district"],
                state = request.POST["state"],
                pincode = request.POST["pincode"],
                companyName = request.POST["companyName"],
                gstin = request.POST["gstin"],
                storeName = request.POST["storeName"],
            )
            seller.save()
            return HttpResponseRedirect("../")
        else:
            return HttpResponseRedirect("register")
    else:
        seller_data = request.session.get("seller")
        if seller_data is not None:
            return render(request, "gstin.html")
        else:
            return HttpResponseRedirect("seller")
            return HttpResponseRedirect("register")
        

def main(request):
    seller = get_seller_from_session(request)
    # print(f"\n --- seller : {seller}")
    if seller is not None:
        return render(request, "main.html", {"seller" : seller})
    else:
        return HttpResponseRedirect("login", {"message": "Something went Worng While Loading"})


def logout(request):
    
    response = HttpResponseRedirect("login")   # using redirect instead of httpresonpse because
    request.session.flush()
    
    response.delete_cookie(settings.SELLER_SESSION_COOKIE_NAME)

    # delete all cookies
    # for cookie in request.COOKIES:
    #     response.delete_cookie(cookie)

    print(f"Cookie Data --->{request.COOKIES}")
    return response

# --- DASHBOARD ---
@xframe_options_sameorigin
def sidebar(request):
    return render(request, "dashboard/sidebar.html")

@xframe_options_sameorigin
def dashboard(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    if request.method == "POST":
        form = request.POST
        product = Product(
            name = form["name"],
            sku = form["sku"],
            price = form["price"],
            stock = form["stock"],
            seller = seller,
            description = form["description"],
            category = form["category"],
        )
        product.save()
        print(f"\n---{product}---")
        print(f"\n---{product.seller}---")
        return HttpResponseRedirect("dashboard") 
    return render(request, "dashboard/dashboard.html", {"products": seller_products, "choices": Product.categories})

@xframe_options_sameorigin
def products(request):
    seller = get_seller_from_session(request)
    seller_products = Product.objects.filter(seller = seller)
    if request.method == "POST":
        form = request.POST
        product = Product(
            name = form["name"],
            sku = form["sku"],
            price = form["price"],
            stock = form["stock"],
            seller = seller,
            description = form["description"],
            category = form["category"],
        )
        product.save()
        print(f"\n---{product}---")
        print(f"\n---{product.seller}---")
        return HttpResponseRedirect("products") 
    return render(request, "dashboard/products.html", {"products": seller_products, "choices": Product.categories})

@xframe_options_sameorigin
def orders(request):
    return render(request, "dashboard/orders.html")

@xframe_options_sameorigin
def customers(request):
    return render(request, "dashboard/customers.html")

@xframe_options_sameorigin
def profile(request):
    seller = get_seller_from_session(request)
    countryCodes = countryCode.objects.all().values()
    seller_dialCode = countryCode.objects.get(dialCode = seller.dialCode)

    if request.method == "POST":
        form_data = request.POST
        
        seller.name = form_data["name"]
        seller.email = form_data["email"]
        seller.dialCode = form_data["dialCode"]
        seller.contact = form_data["contact"]
        seller.password = form_data["password"]
        seller.address = form_data["address"]
        seller.city = form_data["city"]
        seller.district = form_data["district"]
        seller.state = form_data["state"]
        seller.pincode = form_data["pincode"]
        seller.companyName = form_data["companyName"]
        seller.gstin = form_data["gstin"]
        seller.storeName = form_data["storeName"]

        seller.save()
        
        return HttpResponseRedirect("profile")
    return render(request, "dashboard/profile.html", {"seller_dialCode" : seller_dialCode, "countryCodes": countryCodes, "seller": seller})

