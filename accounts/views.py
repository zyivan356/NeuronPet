from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.timezone import now


User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        return redirect('/')
    return render(request, 'users/register.html', {'form': form})


def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
    return redirect('/')

'''
def other_account(request, account_id):
    user = User.objects.get(id=account_id)
    user_courses = Course.objects.filter(author=user).order_by("-pubdate")
    return render(request, 'users/other_profile.html', {'user': user, 'user_courses': user_courses})
'''





