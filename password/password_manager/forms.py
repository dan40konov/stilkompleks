from django import forms
from django.forms import ModelForm
from .models import AddAccount


# class AddAccountForm(forms.ModelForm):
#     class Meta:
#         model = AddAccount
#         fields = [
#             'category', 
#             'other_account',
#             'user_name', 
#             'password', 
#             'confirm_password', 
#         ]

#         widgets = {

#             'password': forms.PasswordInput(),
#             'confirm_password': forms.PasswordInput()
#         }

class AddAccountForm(forms.ModelForm):
    PASSWORD_CATEGORIES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('gmail', 'Gmail'),
        ('others', 'Others')
    )

    category = forms.ChoiceField(choices=PASSWORD_CATEGORIES)
    other_account = forms.CharField(max_length=30, required=False)
    user_name = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = AddAccount
        fields = [
            'category', 
            'other_account',
            'user_name', 
            'password', 
            'confirm_password', 
        ]

    def clean(self):
        cleaned_data = super().clean()
        pass1 = self.cleaned_data['password']
        pass2 = self.cleaned_data['confirm_password']

        if pass1 != pass2:
            raise forms.ValidationError("Both passwords doesn't match")