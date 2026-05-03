from .models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignupSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "username", "email", "password", "password_confirm"]
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate(self, attrs):
        password = attrs.get("password")
        username = attrs.get("username")
        password_confirm = attrs.get("password_confirm")

        errors = {}

        if not password:
            errors["password"] = "Parol kiritilmadi"
        elif len(password) < 8:
            errors["password"] = "Parol kamida 8 ta belgidan iborat bo‘lishi kerak"

        if password and password_confirm and password != password_confirm:
            errors["password_confirm"] = "Parollar mos emas"

        if password and username:
            if username.lower() in password.lower():
                errors["password"] = "Parol username bilan o‘xshash bo‘lmasligi kerak"

        if errors:
            raise ValidationError(errors)

        return attrs


    def create(self, validated_data):
        validated_data.pop("password_confirm")

        user = CustomUser.objects.create_user(**validated_data)
        return user


    def validate_email(self, value):
        if not value or "@" not in value:
            raise ValidationError("Email noto‘g‘ri")

        if value.count("@") != 1:
            raise ValidationError("Email noto‘g‘ri")

        local, domain = value.split("@")

        if not local or not domain:
            raise ValidationError("Email noto‘g‘ri")

        if "." not in domain:
            raise ValidationError("Domain noto‘g‘ri")

        if len(value) < 6 or len(value) > 254:
            raise ValidationError("Email uzunligi noto‘g‘ri")

        return value