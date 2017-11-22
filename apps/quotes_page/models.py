# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['name']) < 2 or len(postData['alias']) < 2:
            errors['name_error'] = 'First and Last name must be 2 or more characters'
            
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not a valid email'
        
        if postData['birthday'] == '':
            errors['birthday'] = 'Please enter your birthday'
        
        if len(postData['password']) < 8 or len(postData['confirm_password']) <8:
            errors['pass_length'] = 'Password must be 8 or more characters'   

        if postData['password'] != postData['confirm_password']:
            errors['pass_match'] = 'Passwords do not match.'          

        if User.objects.filter(email=postData['email']):
            errors['exists'] = "Email already in use."   
        return errors

    def login(self, postData):
        error ={}
        user_to_check = User.objects.filter(email=postData['email'])
        if len(user_to_check) >0:
            user_to_check = user_to_check[0]
            if bcrypt.checkpw(postData['password'].encode(), user_to_check.password.encode()):
                user = {"user" : user_to_check}
                return user
            else:
                errors = {"error":"Email/Password Invalid"}
                return errors
        else:
            errors = {"error":"Login Invalid"}
            return errors
class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    birthday = models.DateField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class QuoteManager(models.Manager):
    def add_quote(self, postData):
        errors = [] 
        if len(postData['author_name']) < 2:
            errors.append("The author must be at least 2 characters")
        if len(postData['quote']) < 10:
            errors.append("The quote must be at least 10 characters.")
        if errors:
            print("Error adding everything")
            return {'errors': errors}
        else:   
            print("Added everything successfully")
            user = User.objects.get(id = int(postData['posted_by']))
            new_quote = self.create(author_name = postData['author_name'], quote = postData['quote'], posted_by = user )
            return {'new_quote': new_quote}

class Quote(models.Model):
    author_name = models.CharField(max_length = 255)
    quote = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    favored = models.ManyToManyField(User, related_name="favored_by")
    posted_by = models.ForeignKey(User, related_name="posted_by")
    objects = QuoteManager()