from django.contrib import admin
from .models import *

class Person_Admin(admin.ModelAdmin):
    list_display = ['image_tag','firstname','lastname', 'user', 'balance']
    list_filter = ['gender']
    readonly_fields = ('image_tag',)
    
admin.site.register(Person, Person_Admin)
