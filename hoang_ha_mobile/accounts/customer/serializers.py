from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .. import models
from datetime import date
User = get_user_model()

class UserUploadImage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "image"
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
        ]
    def validate_birthday(self, bd): #bd = birthday
        today = date.today()
        age = today.year - bd.year
        if (not(0 < age < 150)):
            raise serializers.ValidationError("Invalid date of birth")
        return bd
    
    def validate_email(self, email):
        return email.lower()
    
    def validate_phone(self, attrs):
        try:             
            if not(len(attrs) == 10):
                raise serializers.ValidationError("Invalid phone number: Phone number have to include ten number")
            return attrs
        except:
            raise serializers.ValidationError("Invalid phone number: Don't include characters")
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['old_password', 'new_password']
        extra_kwargs = {
            'old_password': {'write_only':True},
            'new_password': {'write_only':True},
        }

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ["id", "address"]

class ProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = User
        fields = [
            "id",
            "full_name",
            "phone",
            "email",
            "birthday",
            "sex",
            'addresses',
            'image',
        ]
