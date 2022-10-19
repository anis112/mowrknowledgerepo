from django import forms

from .models import Organization


class OrganizationForm(forms.ModelForm):
    organization_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
                "id": "organizationName"
            }
        ))
    short_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control",
                "id": "shortName"
            }
        ))
    mailing_address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address",
                "class": "form-control",
                "id": "mailingAddress"
            }
        ))
    web_address = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "placeholder": "Web Address",
                "class": "form-control",
                "id": "webAddress"
            }
        ))
    organization_chief = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        ))
    chief_designation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Designation",
                "class": "form-control"
            }
        ))
    focal_person = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        ))
    fp_designation = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Designation",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    phone_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "form-control"
            }
        ))
    mobile_no = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Mobile",
                "class": "form-control"
            }
        ))
    logo = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = Organization
        #fields = '__all__'
        fields = [
            'organization_name',
            'short_name',
            'mailing_address',
            'web_address',
            'organization_chief',
            'chief_designation',
            'focal_person',
            'fp_designation',
            'email',
            'phone_no',
            'mobile_no',
            'logo'
        ]
