# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import date, datetime

# Create your models here.
class UserManager(models.Manager):
    def validate_login(self, post):
        #step 1 is look up the user based on the email
        user = User.objects.filter(username=post['username']).first()
        if user and bcrypt.checkpw(post['password'].encode(), user.password.encode()):
        #can't do session here
            return { 'status': True, 'user': user }
        else:
            return { 'status': False, 'error': 'Invalid Credentials: Either Username or Password is incorrect!'}

    def validate_registration(self, post):#every class function must take in self. now add in post data
        #step 1: validate the form data
        #before to access name it was request.POST['name'], but now its post['name'] 
        errors = []
        if post['first_name'] == '':
            errors.append('First Name can not be blank')
        if post['last_name'] == '':
            errors.append('Last Name can not be blank')
        if post['username'] == '':
            errors.append('Username can not be blank')
        if post['email'] == '':
            errors.append('Email can not be blank')
        if post['dob'] >= str(datetime.now()):
            errors.append('Date of birth cannot be in the future')

        username = User.objects.filter(username=post['username']).first()
        email = User.objects.filter(email=post['email']).first()

        if username:
            errors.append('Username already exists')
        if email:
            errors.append('Email already exists')
        if len(post['password']) < 4:
            errors.append('Password must be at least four character')
        elif post['password'] != post['password_confirmation']:
            errors.append('Passwords do not match')
        #step 2: if invalid create error messages
        if not errors:
            user = User.objects.create(
                first_name=post['first_name'],
                last_name=post['last_name'],
                username=post['username'],
                email=post['email'],
                password= bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt(10))
            )
            return {'status': True, 'user': user}#return object with its key as status. if created user, status should be true
        else:
            return {'status': False, 'errors': errors}#if status false, return errors object
        #step 3 if valid is true, create the user and save it to session

    def current_user(self, request):
        return self.get(id=request.session['id'])


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    def __repr__(self):
        return "<User {} {} {} {} {} {}>".format(self.id, self.first_name, self.last_name, self.username, self.email, self.password)

class ItemManager(models.Manager):
    def validate(self, post):
        errors = []

        # Title
        if post['title'] == '':
    #or if len(post['title]) == 0:
            errors.append('Title is Required')
        # Published Date
        if post['published_date'] == '':
    #or if len(post['published_date]) == 0:
            errors.append('Published date is Required')
        else:
            # print post['published_date']
            pub_date = datetime.strptime(post['published_date'], "%Y-%m-%d")# database defaults to this format #unicode. Turn str date into an object.
            current_date = datetime.now()
            #strptime is a method of datetime. Converts a str date to an actual datetime object.

            if pub_date > current_date:
                errors.append('Published date must be in the past.')

        return errors
    def create_item(self, post, user):
        return self.create(
            title = post['title'],
            published_date = post['published_date'],
            creator = user,
        )
        # user = User.objects.get(id=user_id)


class Item(models.Model):
    title = models.CharField(max_length=100)
    published_date = models.DateField()

    creator = models.ForeignKey(User, related_name='items')#'item' has a 'creator' and 'user' has 'items'
    wishlists = models.ManyToManyField(User, related_name="favorite_items")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = ItemManager()

    def __repr__(self):
        return "<Item {} {} >".format(self.title, self.published_date)