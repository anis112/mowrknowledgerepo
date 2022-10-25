from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
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
    
class ChangeCustomUserForm(UserChangeForm):
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_organization_admin', 'organization')
        })
    )
    class Meta:
        model = CustomUser
        fields = '__all__'
        # fields = (
        #          'email',
        #          'first_name',
        #          'last_name'
        #         )
        exclude = ['password','username','is_staff', 'is_superuser', 'user_permissions','last_login', 'date_joined']
        