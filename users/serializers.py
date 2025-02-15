from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'is_verified')
        read_only_fields = ('is_verified',)

    def create(self, validated_data):
        user = User.objects.create_user( # create_user is used instead of create to properly hash the password
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user