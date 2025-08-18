from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required= True, write_only= True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = User( 
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            bio=validated_data.get('bio', ''),
            profile_picture = validated_data.get('profile_picture', None),
        )
        user.set_password(validated_data['password'])
        user.save()

        Token.objects.create(user = user)
        return user
        
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)