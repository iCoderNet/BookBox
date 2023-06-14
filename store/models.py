from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
class Author(models.Model):
    name = models.CharField(max_length=255)
    image  = models.ImageField(upload_to="image/author",blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
class Book(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, models.CASCADE, blank=True, null=True) 
    author = models.ForeignKey(Author, models.CASCADE, blank=True, null=True) 
    image = models.ImageField(upload_to="image/book")
    document = models.FileField(upload_to="document/book", blank=True, null=True)
    doc_code = models.CharField(max_length=250, blank=True, null=True)
    date = models.IntegerField(default=0)
    recommended = models.BooleanField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class WishList(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    
class LastBook(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)