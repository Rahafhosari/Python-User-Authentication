from django.shortcuts import render, redirect
from . import models
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.
def root(request):
    print("Session:",request.session)
    return render(request,'index.html')

def home_page(request):
    if 'logged_user_id' in request.session:
        context = {
            'user_name':request.session['user_name'],
            'user_id':request.session['logged_user_id'],
        }
        return render(request,'home_page.html',context)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        errors = models.User.objects.register_validator(request.POST) #get list of errors 
        if len(errors)>0: #if errors exist loop over the dictionary and show the messages
            for key,value in errors.items():
                messages.error(request, value) #show the messages value
            return redirect('/') 
        else: #if there are no errors --> create new user 
            if request.POST['password'] == request.POST['password_confirm']:                    
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
                print(pw_hash)
                new_user = models.create_user(request.POST, pw_hash)    
                if new_user is not None:
                    if not request.session:  
                        print(request.session)
                        request.session['logged_user_id'] = new_user.id
                        request.session['user_name'] = new_user.first_name
                    return redirect('/home')
    return redirect("/") # never render on a post, always redirect!    

def login(request):
    if request.method == 'POST':
        errors = models.User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            # see if the username provided exists in the database
            user = models.logged_user(request.POST)   #if we use get and empty get returns none
            if user: # note that we take advantage of truthiness here: an empty list will return false / for 'get' we use if user is not None:
                logged_user = user[0] 
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    # if we get True after checking the password, we may put the user id in session
                    request.session['logged_user_id'] = logged_user.id
                    request.session['user_name'] = logged_user.first_name
                    return redirect('/home')
            return redirect('/')
    return redirect('/')

def logout(request): 
    # request.session.clear()
    request.session.flush()
    return redirect('/')

#reference: https://stackoverflow.com/questions/6923027/disable-browser-back-button-after-logout
# from django.views.decorators.cache import cache_control
# @cache_control(no_cache=True, must_revalidate=True)

# def register(request):
#     if request.method == 'POST':
#         print(request.POST)
#         errors = models.User.objects.register_validator(request.POST) #get list of errors 
#         print(errors)
#         if len(errors)>0: #if errors exist loop over the dictionary and show the messages
#             for key,value in errors.items():
#                 print('VALUE:',value)
#                 print('KEY:',key)
#                 print("*****",errors.items())
#                 print("*****",errors.keys())
#                 print("*****",errors.values())
#                 print("*****",errors) #prints dictionary of errors 
#                 print("*****",errors['first_name'])  #First Name should be more than 2 characters.
#                 messages.error(request, value) #show the messages value
#                 print("&&&&&&&",messages.error(request, key,value))
#                 print("%%%%%%%",messages)
#             return redirect('/') 
#         else: #if there are no errors --> create new user 
#             if request.POST['password'] == request.POST['password_confirm']:                    
#                 password = request.POST['password']
#                 pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()  # create the hash    
#                 print(pw_hash)
#                 new_user = models.create_user(request.POST, pw_hash)    
#                 if new_user is not None:
#                     if not request.session:  
#                         print(request.session)
#                         request.session['logged_user_id'] = new_user.id
#                         request.session['user_name'] = new_user.first_name
#                     return redirect('/home')
#     return redirect("/") # never render on a post, always redirect!    

# def login(request):
    # if request.method == 'POST':
    #     errors = models.User.objects.login_validator(request.POST)
    #     if len(errors) > 0:
    #         for key, value in errors.items():
    #             messages.error(request, value)
    #         return redirect('/')
    #     else:
    #         # see if the username provided exists in the database
    #         user = models.logged_user(request.POST)   #if we use get and empty get returns none
    #         if user: # note that we take advantage of truthiness here: an empty list will return false / for 'get' we use if user is not None:
    #             logged_user = user[0] 
    #             if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
    #                 # if we get True after checking the password, we may put the user id in session
    #                 print("$$$$$$$",request.session.keys())
    #                 print("$$$$$$$",request.session.values())
    #                 request.session['logged_user_id'] = logged_user.id
    #                 print("USER ID:",request.session['logged_user_id'])
    #                 request.session['user_name'] = logged_user.first_name
    #                 print("USER NAME:",request.session['user_name'])
    #                 return redirect('/home')
    #         return redirect('/')
    # return redirect('/')