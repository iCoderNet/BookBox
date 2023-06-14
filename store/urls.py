from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homePage, name='home'),
   
    #BOOK STORE
    path('book/', BookInfo, name='bookInfo'),
    path('book/<int:pk>', BookInfo),
    path('book/read/', bookRead, name='bookRead'),
    path('book/read/<int:pk>', bookRead),
    path('book/download/', bookDownload, name='bookDownload'),
    path('book/download/<int:pk>', bookDownload),
    
    path('search/', pageSearch, name='search'),
    
    path('wishlist/', pageWishList, name='WishList'),
    path('wishlist/add/', addWishList, name='addWishList'),
    path('wishlist/add/<int:pk>', addWishList),
    
    
    path('404/', pfn404, name='PNF404'),
    path('contact/', contact, name='contact'),
    
    
    path('<str:html>', html_viewer)
]
