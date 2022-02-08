from django.contrib import admin

from .models import Category, Pet, Catordog, Gender, Classification_pet


admin.site.register(Classification_pet)
admin.site.register(Category)
admin.site.register(Pet)

