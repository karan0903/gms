from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from management.models import Category

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('not valid')
        if form.is_valid():
            print('valid')
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
