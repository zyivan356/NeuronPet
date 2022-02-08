from django.db import models
from django.conf import settings
from django.urls import reverse

class Catordog(models.Model):
    name = models.CharField("Вид животного", max_length=20)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField("Гендер", max_length=20)

    def __str__(self):
        return self.name

class Classification_pet(models.Model):
    image = models.FileField(upload_to='media/classification_pet/', verbose_name='Фото питомца')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "pet"
        verbose_name_plural = "pets"



class Pet(models.Model):
    catordog = models.ForeignKey(Catordog, verbose_name='Кошка или собака', on_delete=models.CASCADE)
    name = models.CharField('Кличка питомца', max_length=20)
    birthday = models.DateField('Дата рождения')
    gender = models.ForeignKey(Gender, verbose_name='Пол питомца', on_delete=models.CASCADE)
    description = models.TextField('Особые приметы')
    image = models.ImageField(upload_to='media/userspets/', verbose_name='Фото питомца')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner', verbose_name="Владелец",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pets:pet_detail', args=[self.id])

class Category(models.Model):
    name = models.CharField("Порода", max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Порода"
        verbose_name_plural = "Породы"
        ordering = ('-name',)

    def get_absolute_url(self):
        return reverse('pets:pets_by_category', args=[self.slug])


