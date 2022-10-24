from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


   
class CustomUserForm(UserCreationForm):
    
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder": "username",
    #             "class": "form-control",
    #             "id": "id_username"
    #         }
    #     ))
    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder": "Email",
    #             "class": "form-control",
    #             "id": "id_email"
    #         }
    #     ))

    

    class Meta:
        model = CustomUser
        #fields = '__all__'
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            # 'is_organization_admin',
            'organization'
           
        ]
    
   