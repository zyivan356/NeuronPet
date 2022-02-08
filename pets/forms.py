from django import forms
from .models import Classification_pet


class PostForm(forms.ModelForm):

    class Meta:
        model = Classification_pet
        fields = ('image', )

