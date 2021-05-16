from rest_framework import serializers
from .models import *


class ObektiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obekti
        fields = ('id', 'name', 'investor', 'address', 'created_at', 'personal_set', 'materialperobekt_set')


class CreateObektiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obekti
        fields = ('name', 'investor', 'address')

class UpdateObektiSerializer(serializers.ModelSerializer):
    id = serializers.CharField(validators=[])

    class Meta:
        model = Obekti
        fields = ('id', 'name', 'investor', 'address')


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ('id', 'name', 'position', 'obekt', 'mail', 'phone_number', 'machine')



        
class CreatePersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personal
        fields = ('id', 'name', 'position', 'obekt', 'mail', 'phone_number', 'machine')


class UpdatePersonalSerializer(serializers.ModelSerializer):
    id = serializers.CharField(validators=[])

    class Meta:
        model = Personal
        fields = ('id', 'name', 'position', 'obekt', 'mail', 'phone_number', 'machine')