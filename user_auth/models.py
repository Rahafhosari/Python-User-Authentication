from django.db import models
import re
import bcrypt
from datetime import date, datetime


class UserManager(models.Manager):
    def register_validator(self, user_info):
        errors = {}
#names
        if(user_info['first_name'].isalpha()) == False:
            errors["first_name"] = "Enter a valid first name."
        if len(user_info['first_name']) <2 :
            errors["first_name"] = "First Name should be more than 2 characters." #["first_name"] is a key for errors dictionary can be any word
        if(user_info['last_name'].isalpha()) == False:
            errors["last_name"] = "Enter a valid last name."
        if len(user_info['last_name']) <2 :
            errors["last_name"] = "Last Name should be more than 2 characters."
#email  
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(user_info['email']): #checking if email matches the regex           
            errors['email'] = "Invalid email address!"
        new_user_email = User.objects.filter(email = user_info['email']) #Unique email in the database
        if len(new_user_email):
            errors['email'] = "Email already exist"
#password
        if len(user_info['password']) < 8:
            errors["password"] = "Password should be at least 8 characters."
        if user_info['password'] != user_info['password_confirm']:
            errors['password_confirm']= "Passwords Don't Match!"
#birthday
        # today = datetime.now().strftime("%Y%m%d")
        # user_birthday = user_info['birthday'].replace("-", "")
        # if len(user_info["birthday"]) > 0 and datetime.strptime(user_info["birthday"], '%Y-%m-%d') >= datetime.today() :
        #     errors["birthday"] = "Invalid Birth date"
        # if (int(today[0:4]) - int(user_birthday[0:4])) <= 13:
        #     errors["birthday"] = "You should be at least 13 years old to register"
        return errors

    def login_validator(self, user_info):
        errors = {}
        # user = User.objects.get(email=request.POST['email'])  # hm...is it really a good idea to use the get method here?
        # if bcrypt.checkpw(request.POST['password'].encode(), user.pw_hash.encode()):
        #     print("password match")
        # else:
        #     print("failed password")
        all_user = User.objects.filter(email = user_info['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(user_info['email']):
            errors['email'] = "Wrong email address!"
        if not len(all_user): #email required
            errors['email'] = "Email Required: Email not registered! /Wrong Email" 
        if len(user_info['password']) < 8:
            errors["password"] = "Password should be 8 characters minimum"
#Password Match the Hashed Password in Database
        if len(all_user) and not bcrypt.checkpw(user_info['password'].encode(), all_user[0].password.encode()):
            errors["password"] = "Wrong Password! / Password doesn't match!"
        else:
            print("password Match")
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255, null = False)
    last_name = models.CharField(max_length=255, null = False)
    email = models.CharField(max_length=255, null = False)
    password = models.CharField(max_length=255, null = False)
    birthday = models.DateField(null=True,blank=True,default="YYYY-MM-DD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


def create_user(data, hashed_password):
    birth_date = data['birthday']
    if not birth_date: 
        birth_date = None
        return User.objects.create(first_name=data['first_name'],last_name=data['last_name'],email=data['email'],password=hashed_password,birthday=birth_date)

#reference: https://stackoverflow.com/questions/20604786/how-to-insert-null-into-djangos-datefield

def logged_user(data):
    return User.objects.filter(email = data['email'])