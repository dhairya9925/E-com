from django.test import TestCase

# Create your tests here.
seller_data= {
    "name_key" : "name_1",
    "email_key" : "email_1",
    "dialCode_key" : "dialCode_1",
    "contact_key" : "email_1",
    "password_key" : "password_1",
}

for data in seller_data:
    print(f"Data : \"{data}\" ")