# django forms- which are generated automatically
from django import forms
from.models import Book
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        # exclude = ('is_active', 'is_staff', 'is_superuser')