# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User, Item
from django.contrib import messages

# Create your views here
def flash_errors(request, errors):
    for error in errors:
        messages.error(request, error)

def index(request):

     return render(request, 'login_registration_app/index.html')

def register(request):
    if request.method == 'POST':
        result = User.objects.validate_registration(request.POST)
        if result['status'] == False:
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['id'] = result['user'].id
            request.session['user_name'] = result['user'].username
            messages.add_message(request, messages.SUCCESS, "Thanks for registering " + request.session['user_name'] + "!. Please login to your account.")
            return redirect('/')

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_login(request.POST)
        if result['status'] == False:
            messages.error(request, result['error'])
            return redirect('/')
        else:
            request.session['id'] = result['user'].id
            return redirect('/dashboard')

def dashboard(request):
    # User.objects.all().delete()
    # Item.objects.all().delete()
    user = User.objects.current_user(request)#current_user defined in models.py line 58
    # items = user.items.all()
    # my_items = Item.objects.filter(creator=user)
    my_items = Item.objects.filter(creator=user)
    favorite_items = user.favorite_items.all()
    other_items = Item.objects.exclude(id__in=my_items).exclude(id__in=favorite_items)

    context = {
        'user' : user,
        # 'items' : items,
        'my_items' : my_items,
        'favorite_items': favorite_items,
        'other_items' : other_items
    }
    # print my_items
    # print favorite_items

    return render(request, 'login_registration_app/dashboard.html', context)

def add(request):

    return render(request, 'login_registration_app/add.html')

def create(request):
    if request.method == "POST":
        #validate form post
        errors = Item.objects.validate(request.POST)# call the method 'validate' inside our ItemManager from models to inside our views. Declared ItemManager overiding object from items. Call in the arguments that validate takes

        #if errors do not exist
        if not errors:
            #get current user
            user = User.objects.current_user(request)

            #create the item
            item = Item.objects.create_item(request.POST, user)# go to def create_item and pass arguments

            #redirect to all items page
            return redirect('/dashboard')

        #flash errors
        flash_errors(request, errors)

    # if request.method == 'POST':
    #     result = Item.objects.validate(request.POST)
    #     if result['status'] == False:
    #         for error in result['errors']:
    #             messages.error(request, error)
    #         return redirect('/add')
    #     else:
    #         item = Items.objects.create_item(request.POST, user)

    return redirect('/wish_items/create')

def delete(request, id):
    # current user
    user = User.objects.current_user(request)

    item = Item.objects.filter(id=id).first()

    if item and user == item.creator:#if item is actually in our database and it was created by user.
        item.delete()

    return redirect('/dashboard')

def favorite(request, id):
    user = User.objects.current_user(request)#tells who is favoriting the item. current_user defined in models.py line 58
    item = Item.objects.filter(id=id).first()

    # print Item.objects.filter(id=id).first().title
    if item:#ManyToMany relationship. Don't have to create it when item or use was entered into database. Use ManyToMany table to add them together. We've already defined item and have our user.
        user.favorite_items.add(item)#add the correct object
   # or item.wishlists.add(user)
        return redirect('/dashboard')

def unfavorite(request, id):
    user = User.objects.current_user(request)
    item = Item.objects.filter(id=id).first()

    if item:#Repeat code for favorite. Change Add to Remove.
        user.favorite_items.remove(item)#removed the correct object
   # or item.wishlists.remove(user)
        return redirect('/dashboard')

def show(request, id):
    # data = {"user" : User.objects.filter(id=id)}
    user = User.objects.current_user(request)
    item = Item.objects.filter(id=id).first()
    wishlists = Item.objects.get(id=id).wishlists.all()
    # wishlists = item.wishlists.all()
    print wishlists
    print item.creator.first_name+' '+item.creator.last_name

    context = {
        'user' : user,
        'item' : item,
        'wishlists' : wishlists
    }

    return render(request, 'login_registration_app/show.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')