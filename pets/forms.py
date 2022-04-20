from django import forms
from .models import Classification_pet, Pet, Catordog, Gender

YEARS = [x for x in range(1992, 2023)]

class PostForm(forms.ModelForm):
    image = forms.FileField(label = "", error_messages={'required': ''}, widget=forms.FileInput(attrs={'class': 'neuron_form2'}))

    class Meta:
        model = Classification_pet
        fields = ('image', )

class PetForm(forms.ModelForm):
    image = forms.FileField(label="Фотография", error_messages={'required': ''},widget=forms.FileInput(attrs={'class': 'pet_form_image', 'id': 'pet_form_image_label'}))
    catordog = forms.ModelChoiceField(Catordog.objects.all(), label="Кошка или собака", error_messages={'required': ''}, widget=forms.Select(attrs={'class': 'pet_form_catordog', 'id': 'pet_form_catordog_label'}))
    name = forms.CharField(label='Кличка', error_messages={'required': ''}, widget=forms.TextInput(attrs={'class': 'pet_form_name', 'id': 'pet_form_name_label'}))
    birthday = forms.DateField(label="Дата рождения", widget=forms.SelectDateWidget(years=YEARS, attrs={'class': 'pet_form_birthday', 'id': 'pet_form_birthday_label'}), error_messages={'required': ''})
    gender = forms.ModelChoiceField(Gender.objects.all(), label="Пол", error_messages={'required': ''}, widget=forms.Select(attrs={'class': 'pet_form_gender', 'id': 'pet_form_gender_label'}))
    description = forms.CharField(label='Особые приметы', error_messages={'required': ''}, widget=forms.TextInput(attrs={'class': 'pet_form_description', 'id': 'pet_form_description_label'}))

    class Meta:
        model = Pet
        fields = ('name', 'gender', 'catordog', 'birthday', 'description', 'image')
