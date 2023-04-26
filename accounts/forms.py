from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,UserChangeForm, PasswordResetForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

   
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
            # 'phone_number',
            # 'designation',
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


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        """
        if not email:
            raise ValidationError(_('Email field is required.'), code='required')
        user_model = get_user_model()
        users = user_model._default_manager.filter(email__iexact=email, is_active=True)
        if not users:
            raise ValidationError(_('Sorry, this email address is not registered in our system.'), code='invalid')
        return users