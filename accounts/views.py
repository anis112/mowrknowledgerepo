from email import message

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as logout_view
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import constants

from accounts.models import CustomUser

from .forms import CustomUserForm, ChangeCustomUserForm
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import ValidationError

User = get_user_model()

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data['username']
            upassword=form.cleaned_data['password']           
            user = authenticate(username=uname, password=upassword)
            if user.is_active:
                if user.is_superuser:
                    auth_login(request,user)
                    return redirect('/admin')  # or your url name
                elif user.is_staff:
                    auth_login(request,user)
                    return redirect('/knowledgebase/dashboard')  # or your url name
                else:
                    auth_login(request,user)
                    return redirect('/knowledgebase/dashboard/')
            else:
                raise ValidationError("This account is inactive.",code='inactive',)
            
                # messages.add_message(request, constants.SUCCESS, 'Invalid username or password ')  
                # form=AuthenticationForm()
                # return render(request, 'login.html',{'form':form})     
    
        else:  
            messages.add_message(request, constants.SUCCESS, 'Invalid username or password ') 
            form=AuthenticationForm()
            return render(request, 'login.html',{'form':form})     

    else:
        if request.user.is_authenticated:
            return redirect('/accounts/profile/'+request.user.username)
        else:
            form=AuthenticationForm()
            return render(request, 'login.html',{'form':form})    

def logout(request):
    logout_view(request)
    return redirect('accounts/login')

def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            auth_login(request,form)
            return redirect('/knowledgebase/dashboard/')             
    else:
        form = CustomUserForm()
        return render(request, 'signup.html', {
        'form': form
        })
@login_required
# @permission_required('polls.add_choice', raise_exception=True)
def user_profile(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, 'user_profile.html', {"user":user})

def user_list(request,organization_id=None,hash=None):
    if request.user.is_superuser:
        return redirect('/admin/accounts/customuser/') 
    elif organization_id==None:
        messages.add_message(request, constants.WARNING, 'You are not a organizational admin user.') 
        return render(request, 'user_list.html')
    #     return HttpResponse(request, 'user_list.html')
    # if hash:
    #     chash = sha1("secret_word%s"%organization_id).hexdigest()
    #     if not chash==hash:
    #         if request.user.is_organization_admin==True:
    #             user_list = CustomUser.objects.filter(organization_id=organization_id)
    #             return HttpResponse(request, 'user_list.html', {"user_list":user_list})
    #         else:    
    #             messages.add_message(request, constants.WARNING, 'You are not a organizational admin user.') 
    #             return render(request, 'user_list.html')
        
    if request.user.is_organization_admin==True:
        user_list = CustomUser.objects.filter(organization_id=organization_id)
        return render(request, 'user_list.html', {"user_list":user_list})
    
        
    
    else:    
        messages.add_message(request, constants.WARNING, 'You are not a organizational admin user.') 
        return render(request, 'user_list.html')

def edit_user(request,id):
    if request.method == 'POST':
        user = CustomUser.objects.get(id=id)
        form = ChangeCustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/knowledgebase/dashboard/')   
    else:    
        
        user = CustomUser.objects.get(id=id)
        form = ChangeCustomUserForm(instance=user)
        return render(request, 'edit_user.html', {"form":form})


# def manage_data(request):
#     return redirect('/admin/') 
    