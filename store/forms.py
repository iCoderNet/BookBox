from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):

   class Meta:
      model = Author
      fields = ['name', 'image', 'description']
      
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ['created_at']
