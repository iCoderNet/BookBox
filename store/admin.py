from django.contrib import admin
from .models import *

admin.site.register([Category, Author, Book, WishList, LastBook])