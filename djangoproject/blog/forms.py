from django import forms
from .models import Posts


class PostCreationForm(forms.ModelForm):

   class Meta:
       model=Posts
       fields=['title', 'content', 'image']


