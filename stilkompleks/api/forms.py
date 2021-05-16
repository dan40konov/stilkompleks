from django import forms
from api.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

class CreatePersonalForm(forms.ModelForm):

    class Meta:
        model = Personal
        fields = fields = ['name', 'position', 'obekt', 'mail', 'phone_number', 'machine', 'image']



class CreateUserFrom(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class OrderMaterialForm(ModelForm):
    class Meta:
        model = OrderMaterial
        fields = ['material', 'amount']

class OrderMatForm(ModelForm):
    class Meta:
        model = OrderMat
        fields = ['date']
class OrderMatFormCompleted(ModelForm):
    class Meta:
        model = OrderMat
        fields = ['complete']

class OrderMatFormTransport(ModelForm):
    class Meta:
        model = OrderMat
        fields = ['transport']
class OrderMatPerObektForm(ModelForm):
    class Meta:
        model = OrderMaterialPerObekt
        fields = ['amount']

class OrderMachineForm(ModelForm):
    class Meta:
        model = OrderMachine
        fields = ['machine', 'hours', 'obekt', 'date']
