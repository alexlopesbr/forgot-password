from core.models import User
from rest_framework import serializers
from core.exceptions import InvalidPassword, EmailAlreadyTaken


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True},
                        'password2': {'write_only': True}}
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)

        if password is not None and not instance.check_password(password2):
            raise InvalidPassword

        if password is not None:
            instance.set_password(password)

        return super().update(instance, validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).count() > 0:
            raise EmailAlreadyTaken

        return value
