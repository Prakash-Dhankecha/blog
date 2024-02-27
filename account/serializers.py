from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'password2']


    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username is already taken')

        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError('Passwords do not match')

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'].lower(),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Account does not exist')

        return data

    def get_jwt_token(self, data):

        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            return {'message': 'Invalid credentials', 'data':{}},

        refresh = RefreshToken.for_user(user)

        return {
            'message': 'Logged in successfully',
            'data': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }

