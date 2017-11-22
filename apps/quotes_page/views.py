# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'quotes_page/index.html')

def process(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            print errors[error]
            messages.error(request, errors[error])
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], birthday = request.POST['birthday'], password = hashed_pw)
        request.session['id'] = user.id
        messages.success(request, "You have successfully registered")        
    return redirect('/quotes')

def login(request):
    login_return = User.objects.login(request.POST)
    if 'user' in login_return:
        request.session['id'] = login_return['user'].id
        messages.success(request, "You have successfully logged in")
        return redirect('/quotes')
    else:
        messages.error(request, login_return['error'])
    return redirect('/')

def users(request, user_id):
    context={"user": User.objects.get(id=user_id)}
    return render(request, 'quotes_page/users.html', context)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
        messages.success(request, "You have logged out")
    return redirect('/')

def add_quote(request):
    if request.method == "POST":
        new_quote = Quote.objects.add_quote(request.POST)
        if 'errors' in new_quote:
            for error in new_quote['errors']:
                print error
                messages.error(request, error)
            return redirect('/quotes')
        else:
            pass 
            return redirect('/quotes') 
    user = User.objects.get(id =request.session['id'])
    context={
        'quotes': Quote.objects.exclude(favored=user),
        'favored': Quote.objects.filter(favored=user),
        'user': user
    }
    return render(request, 'quotes_page/quotes.html', context)

def add_fav(request, quote_id):
    quote = Quote.objects.get(id = quote_id)
    user = User.objects.get(id =request.session['id'])
    quote.favored.add(user)
    return redirect('/quotes')

def unlike(request, quote_id):
    quote = Quote.objects.get(id = quote_id)
    user = User.objects.get(id =request.session['id'])
    quote.favored.remove(user)
    return redirect('/quotes')