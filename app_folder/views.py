from django.shortcuts import render,redirect,HttpResponse
from .models import *
import bcrypt
from django.contrib import messages
from datetime import datetime
import pytz

def mainpage(request):
    return render(request,"page_1.html")

def success(request):
    user_id = request.session.get('user_id')
    if user_id:
        context = {
            'user' : User.objects.get(id=user_id),
            'quotes' : FavoriteQuote.objects.all().order_by("-id"),
        }
        return render(request,"page_2.html",context)
    else:
        return redirect('/')

def register(request):
    errors = User.objects.registerValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session.flush()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        email = request.POST['email']
        password = request.POST['password']
        password_bcrypt = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name,last_name=last_name,birthday=birthday,email=email,password=password_bcrypt)
        request.session['user_id'] = user.id
        return redirect('/success')

def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        request.session.flush()
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)[0]
        request.session['user_id'] = user.id
        return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')

def add_favorite_quote(request):
    user_id = request.session.get('user_id')
    if user_id:
        errors = User.objects.quoteValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
        else:        
            user = User.objects.get(id=user_id)
            quote = request.POST['quote']
            author = request.POST['author']
            favorite_quote = FavoriteQuote.objects.create(quote=quote,author=author,added_by=user)
            favorite_quote.save()
            favorite_quote.liked_by.add(user)
        return redirect('/success')
    else:
        return redirect('/')

def all_quotes_by_user(request,quote_added_by_id):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        other_user = User.objects.get(id=quote_added_by_id)
        context = {
            'user' : user,
            'other_user' : other_user,
            'quotes' : other_user.quotes.all().order_by("-id"),
        }
        return render(request,'page_3.html',context)
    else:
        return redirect('/')

def like_quote(request,quote_id,page_number):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        quote = FavoriteQuote.objects.get(id=quote_id)
        if quote in user.liked_quotes.all():
            user.liked_quotes.remove(quote)
        else:
            user.liked_quotes.add(quote)
        user.save()
        if page_number == 2:
            return redirect('/success')
        elif page_number == 3:
            return redirect('/all_quotes_by_user/'+str(quote.added_by.id))
        elif page_number == 5:
            return redirect('/display_user_information')
        elif page_number == 6:
            return redirect('/edit_user_information')
    else:
        return redirect('/')

def delete_quote(request,quote_id,page_number):
    user_id = request.session.get('user_id')
    if user_id:
        quote = FavoriteQuote.objects.get(id=quote_id)
        other_user_id = quote.added_by.id
        quote.delete()
        if page_number == 2:
            return redirect('/success')
        elif page_number == 3:
            return redirect('/all_quotes_by_user/'+str(other_user_id))
        elif page_number == 5:
            return redirect('/display_user_information')
        elif page_number == 6:
            return redirect('/edit_user_information')
    else:
        return redirect('/')

def display_user_information(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'quotes' : user.quotes.all().order_by("-id"),
        }
        return render(request,'page_5.html',context)
    else:
        return redirect('/')

def edit_user_information(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(id=user_id)
        context = {
            'user' : user,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'birthday' : str(user.birthday),
            'email' : user.email,        
            'quotes' : user.quotes.all().order_by("-id"),
        }
        return render(request,'page_6.html',context)
    else:
        return redirect('/')

def update_user_information(request):
    user_id = request.session.get('user_id')
    if user_id:
        errors = User.objects.updateUserValidator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/edit_user_information')
        else:  
            user = User.objects.get(id=user_id)
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return redirect('/success')
    else:
        return redirect('/')
