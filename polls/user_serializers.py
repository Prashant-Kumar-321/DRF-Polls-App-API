"""
Contains a serializer to create a User

"""
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.ModelSerializer):
    """Create new user"""

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

        extra_kwargs = {
            'password': {
                'write_only': True # used only during creating or updating a new user
            }
        }

    def validate_password(self, value): 
        """Check password strong using django's built-in validation method"""
        validate_password(value)
        return value

    def validate_email(self, value): 
        """ Check email uniqueness """

        if User.objects.filter(email=value).exists(): 
            raise serializers.ValidationError('A user with this email already exists')
    
        return value

    def validate(self, data):
        """Global validation method
            Validate if password and password2(Confirm password equal)
        """

        if data['password'] != data['password2']: 
            raise serializers.ValidationError('Password and confirm password does not match')

        return super().validate(data)


    def create(self, validated_data):
        user = User(
            username=validated_data['username'], 
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])

        user.save()

        # Create a token for the user
        Token.objects.create(user=user)

        return user

