from django.urls import path, include
from .views import *

urlpatterns = [
    path('', adminDashPage, name='adminDash'),
    #CATEGORY
    path('category/', adminCatPage, name='adminCat'),
    path('category/add/', addCatPage, name='addCat'),
    path('category/edit/', editCatPage, name='editCat'),
    path('category/edit/<int:id>', editCatPage),
    path('category/delete/', delCatPage, name='delCat'),
    path('category/delete/<int:id>', delCatPage),
    #AUTHOR
    path('author/', adminAuthorPage, name='adminAuthor'),
    path('author/add/', addAuthorPage, name='addAuthor'),
    path('author/edit/', editAuthorPage, name='editAuthor'),
    path('author/edit/<int:id>', editAuthorPage),
    path('author/delete/', delAuthorPage, name='delAuthor'),
    path('author/delete/<int:id>', delAuthorPage),
    #BOOK
    path('book/', adminBookPage, name='adminBook'),
    path('book/add/', addBookPage, name='addBook'),
    path('book/edit/', editBookPage, name='editBook'),
    path('book/edit/<int:id>', editBookPage),
    path('book/delete/', delBookPage, name='delBook'),
    path('book/delete/<int:id>', delBookPage),
    #USER
    path('user/', adminUser, name='adminUser'),
    path('user/add/', addUserPage, name='addUserPage'),
    path('user/edit/', editUserPage, name='editUserPage'),
    path('user/edit/<int:pk>', editUserPage),
    path('user/delete/', delUserPage, name='delUserPage'),
    path('user/delete/<int:pk>', delUserPage),
    
]
