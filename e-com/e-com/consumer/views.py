from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import users
from core.models import Orders, Product
from mysite import settings
import os
import uuid

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
        # print(f"--- User: {user} ---")
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


        print(f"\n\n\n--- Products: {products} ---")
        # print(f"default session_id ---> {request.COOKIES.get("sessionid")}")
        # print(f"Cookie Data --->{request.COOKIES}")
        # print(f"custom user session_id ---> {request.session.items()}")
        return render(request, "home.html", {"name": user.name, "products": products})
    else:
        print("--- NOT LOGGED IN ----")
        # print(f"--- NOT LOGGED {{ user }} ----")
        return render(request, "home.html", {"products": products})


def cart(request):
    user = get_user_from_session(request)
    if user is not None:
        return render(request, "cart.html", {"name": user.name, "order": user.order})
        return render(request, "cart.html", {"name": user.name, "order": user.order, "products": user.order.products})
    else:
        return render(request, "cart.html")


def logout(request):

    response = HttpResponseRedirect("../login")   # using redirect instead of httpresonpse because
    request.session.flush()
    
    response.delete_cookie(settings.USER_SESSION_COOKIE_NAME)

    # delete all cookies
    # for cookie in request.COOKIES:
    #     response.delete_cookie(cookie)

    print(f"Cookie Data --->{request.COOKIES}")
    return response

# def profile(request):
#     user = get_user_from_session(request)
#     if not user:
#         return HttpResponseRedirect("../login")  
#     if request.method == "POST":
#         if "Profile" in request.POST:
#             print(f"--- PROFILE FORM POST ---")
#             user.name = request.POST["name"]
#             user.email = request.POST["email"]
#             user.password = request.POST["password"]
#             if request.POST["contact"] is not None:
#                 user.contact = request.POST["contact"]

#             user.save()

#             return HttpResponseRedirect("../profile")
#         elif "deleteAccount" in request.POST:
#             print(f"--- DELETE ACCOUNT FORM POST ---")
#             user = get_user_from_session(request)
#             if request.POST["password"] == user.password:
#                 print(f"--- User({user.name}) Deleted ---")
#                 # user.delete()
#                 request.session.flush()
#                 return HttpResponseRedirect("../")
#             else:
#                 return render(request, "profile.html", {"message": "Password didn't match!!"})
#     else:
#         return render(request, "profile.html", {"user": user})


def profile(request):
    # Get the user from the session
    user = get_user_from_session(request)
    
    # If the user is not logged in, redirect to login
    if not user:
        return HttpResponseRedirect("../login")
    
    if request.method == "POST":
        # Handling Profile Update
        if "Profile" in request.POST:
            print(f"--- PROFILE FORM POST ---")
            
            # Update user data with form values
            user.name = request.POST.get("name", user.name)
            user.email = request.POST.get("email", user.email)
            user.password = request.POST.get("password", user.password)
            user.contact = request.POST.get("contact", user.contact)  # Only update contact if provided

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

        print(f"-- POST data: {request.POST} --")
    # Handling GET request or when no POST action is triggered
    return render(request, "profile.html", {"user": user})

def deleteAccount(request):
    user = get_user_from_session(request)
    print(f"--- User({user.name}) Deleted ---")
    # user.delete()
    request.session.flush()
    return HttpResponseRedirect("../")
# -------------------------------------------------------------------------------------------------------------------------
