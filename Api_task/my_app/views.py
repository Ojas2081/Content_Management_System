from django.shortcuts import render
import requests


from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login as auth_login

from django.contrib.auth import authenticate

# Create your views here.

from django.http import JsonResponse, HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from .serializers import *
import sys
from django.db import connection
import os
import json
from django.contrib.sites.shortcuts import get_current_site


def upperstr(string):
    for ele in string:
        if ele.isupper():
            return True
    return False


def lowerstr(string):
    for ele in string:
        if ele.islower():
            return True
    return False


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["post"], url_path="login", permission_classes=(AllowAny,))
    def login(self, request):
        try:
            data = request.data

            email = data.get("email", None)
            password = data.get("password", None)

            user = authenticate(email=email, password=password)
            # auth_login(request, user)

            # if user:
            #     # response = [{
            #     #     "message": "A user with this email already exists."
            #     #     }]
            #     # status_ = status.HTTP_400_BAD_REQUEST
            # else:
            #     user = User.objects.create(**data)
            #     user.set_password(password)
            #     user.is_active = True
            #     user.save()

            ################## TOKEN OBTAIN PAIR #######################

            site = get_current_site(request)
            # print(url)
            url = "http://{}/token/".format(site)
            print(url)
            data = {"email": email, "password": password}
            print(data)
            response = requests.post(url, data=data)
            print(response)

            ################## TOKEN OBTAIN PAIR #######################
            response = [{"email": email, "access_token": response.json()["access"]}]
            status_ = status.HTTP_201_CREATED
        except Exception as error:
            response = [{"Error": "Error is there"}]
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            print("Register line number of error is {}".format(sys.exc_info()[-1].tb_lineno), error)
        return HttpResponse(response, status=status_)

    @action(detail=False, methods=["post"], name="author_register")
    def author_register(self, request, *args, **kwargs):
        try:
            print("entryyyyyyyyyyyyyy")
            address = ""
            city = ""
            state = ""
            country = ""
            received_json_data = json.loads(request.body)
            print(received_json_data, "asasasas")
            for auth_key, val in received_json_data.items():
                if auth_key == "email":
                    if val == "":
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {"Error": "Email Id required"}
                        return JsonResponse(dict, status=status_)
                    email = val
                if auth_key == "password":
                    print(val == "")
                    print(upperstr(val))
                    print(lowerstr(val))
                    print(len(val) < 8)
                    if val == "" or (not upperstr(val)) or (not lowerstr(val)) or len(val) < 8:
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {
                            "Error": "Password should be greater than 8 letters and should have 1 uppercase and 1 lowercase"
                        }
                        return JsonResponse(dict, status=status_)
                    else:
                        password = val
                        print(password, "1111111111")

                if auth_key == "full_name":
                    if val == "":
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {"Error": "Your full name is mandatory"}
                        return JsonResponse(dict, status=status_)
                    else:
                        full_name = val

                if auth_key == "phone":
                    if val == "" or len(val) != 10:
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {"Error": "length of phone number should be excatly 10"}
                        return JsonResponse(dict, status=status_)
                    else:
                        phone = val

                if auth_key == "role":
                    if val == "":
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {"Error": "Role is mandatory"}
                        return JsonResponse(dict, status=status_)
                    else:
                        role = val.lower()

                if auth_key == "Address":
                    address = val

                if auth_key == "city":
                    city = val

                if auth_key == "state":
                    state = val

                if auth_key == "country":
                    country = val

                if auth_key == "pincode":
                    if val == "" or len(val) != 6:
                        status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
                        dict = {"Error": "length of pincode should be exactly 6"}
                        return JsonResponse(dict, status=status_)
                    else:
                        pincode = val

            usr = User()
            usr.email = email
            usr.set_password(password)
            usr.full_name = full_name
            usr.phone = phone
            usr.role = role
            usr.address = address
            usr.city = city
            usr.state = state
            usr.country = country
            usr.pincode = pincode
            usr.save()

            from django.db import connection

            cursor = connection.cursor()
            cursor.execute(""" Select * from my_app_user """)
            myquery = cursor.fetchall()
            print("this is my output=========", myquery)
            response_data = []
            dict = {}

            dict["my_data"] = myquery

            message = "Success"
            status_ = status.HTTP_200_OK

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(error))
            message = error
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            dict = {"Error": "Failure while UPDATING."}
        return JsonResponse(dict, status=status_)


class ContentViewSet(viewsets.ModelViewSet):

    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    @action(detail=False, methods=["get"], name="get_queryset", permission_classes=(IsAuthenticated,))
    def get_queryset(self):
        if self.request.user.role == "author":
            queryset = self.queryset.filter(author=self.request.user.email)
        else:
            queryset = self.queryset
        print(queryset)
        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ContentSerializer(queryset, many=True)
        response = [{"results": serializer.data}]
        status_ = status.HTTP_200_OK
        return JsonResponse(response, safe=False)

    @action(detail=False, methods=["get"], name="admin_view")
    def admin_view(self, request, *args, **kwargs):
        try:
            # from django.db import connection
            cursor = connection.cursor()
            # cursor.execute(''' Select * from Country ''')
            cursor.execute(""" Select * from my_app_content """)
            myquery = cursor.fetchall()
            print(len(myquery))
            print("this is my output=========", myquery)
            # print("11111111111111111")
            j = 0
            response_data = []
            dict = {}

            dict["my_data"] = myquery

            message = "Success"
            status_ = status.HTTP_200_OK

        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(str(error))
            message = error
            status_ = status.HTTP_500_INTERNAL_SERVER_ERROR
            dict = {"Error": "Failure while UPDATING."}
        return JsonResponse(dict, status=status_)


def seeding_data():
    import pandas as pd

    data = pd.read_csv("seeding_data.csv")
    print("got file")
    from .models import User

    for i in range(data.shape[0]):

        user = User.objects.create(
            email=data.loc[i, "email"],
            full_name=data.loc[i, "full_name"],
            phone=data.loc[i, "phone"],
            address=data.loc[i, "address"],
            city=data.loc[i, "city"],
            state=data.loc[i, "state"],
            country=data.loc[i, "country"],
            pincode=data.loc[i, "pincode"],
            role="admin",
        )
        # data.loc[i, "password"]
        user.set_password("abcd12345")
        user.save()
