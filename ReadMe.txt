1) Create a virtual environment
2) activate the environment 
3) Then type pip install -r requirements.txt
4) Then python manage.py runserver
5) Then hit following API's first register the user
6) http://127.0.0.1:8000/api/user/author_register/

in POST

 {
        "email": "ojas@gmail.com",
        "password": "Ojas1234",
        "full_name": "Ojas Acharekar",
        "phone": "1234567890",
        "address": "",
        "city": "",
        "state": "",
        "country": "",
        "pincode": "400002",
        "role": "author",
    }

then use http://127.0.0.1:8000/api/user/login/

to login but pass in raw data the needed information
 {
        "email": "ojas@gmail.com",
        "password": "Ojas1234",
}

then hit the API in post
you will recieve a token use that token as authentication token in bearer token field.

then use http://127.0.0.1:8000/api/adm/
as GET to view all the content

http://127.0.0.1:8000/api/adm/
as POST to post the content  
with the required format as in get in raw data

for update delete use http://127.0.0.1:8000/api/adm/1/
put id at the end and then select suitable request of PUT, PATCH, DELETE

Token is mandatory for every process.

