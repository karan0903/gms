from django.shortcuts import render
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print(form.data["username"])
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You are now able to login.')
            return redirect('login')
    else:
        print('hello world')
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
