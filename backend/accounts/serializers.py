# accounts/serializers.py
from django.contrib.auth.models import User # Or your custom user model
from rest_framework import serializers

# Example: Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    class Meta:
        model = User # Use settings.AUTH_USER_MODEL if you have a custom user
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # Add more validation if needed (e.g., email uniqueness checked by model)
        return attrs

    def create(self, validated_data):
        # Create the user instance
        user = User.objects.create_user( # use create_user to hash the password
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Example: Serializer for displaying user details
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User # Use settings.AUTH_USER_MODEL
        fields = ['id', 'username', 'email', 'first_name', 'last_name'] # Only expose non-sensitive fields