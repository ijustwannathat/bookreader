from rest_framework import serializers

from bookstorage.serializers import BookUserSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    books = BookUserSerializer(many=True, required=False)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
            "email",
            "books",
        ]
        read_only_fields = ["books"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.pop("password2")
        if password != password2:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
