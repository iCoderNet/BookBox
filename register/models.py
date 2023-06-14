from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe



class Person(models.Model):
    GENDER = (
                ('1', 'Erkak'),
                ('2', 'Ayol'),
            )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/person/", default='image/person/08.jpg')
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    balance = models.IntegerField(default=0)
    
    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

    def image_tag(self):
        return mark_safe('<img src="{}" height=50 />'.format(self.image.url))