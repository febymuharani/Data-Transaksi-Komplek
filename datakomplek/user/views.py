from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.http import HttpResponseNotAllowed
from django.contrib.auth import logout
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context = {
        'form' : form,

    }
    return render(request, 'user/register.html', context)

def LogoutView(request):
        logout(request)
        return redirect('user-login') 
