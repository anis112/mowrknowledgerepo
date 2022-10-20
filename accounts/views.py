from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_view
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upassword=form.cleaned_data['password']           
            user = authenticate(username=uname, password=upassword)
            if user.is_active:
                if user.is_superuser or user.is_staff:
                    auth_login(request,user)
                    return redirect('/knowledgebase/dashboard/')  # or your url name
                else:
                    auth_login(request,user)
                    return redirect('/')

    else:
        form=AuthenticationForm()
        return render(request, 'login.html',{'form':form})    

def logout(request):
    logout_view(request)
    return redirect('accounts/login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {
        'form': form
    })
