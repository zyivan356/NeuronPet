from django.urls import path
from pets.views import main, pets_owner_list, pet_detail, neuron_network, pet_create

urlpatterns = [
    path('', main, name='main'),
    path('mypets/', pets_owner_list, name='pets_owner_list'),
    path('pet/<int:id>/', pet_detail, name='pet_detail'),
    path('pet_neuron/', neuron_network, name="neuron_network"),
    path('pet_add/', pet_create, name="pet_create"),
]

