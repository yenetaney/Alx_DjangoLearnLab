from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required= True, write_only= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

        def create(self, validate_data):
            user = User( 
                username = validate_data['username'],
                email = validate_data('email', ''),
                bio = validate_data('bio', ''),
                profile_picture = validate_data('profile_picture', None),
            )
            user.set_password(validate_data['password'])
            user.save()

            Token.objects.create(user = user)
            return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)