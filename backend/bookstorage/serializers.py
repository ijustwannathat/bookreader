from rest_framework import serializers

from .models import Book


class BookSeriazlier(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Book
        fields = "__all__"

    def validate_file(self, file):
        if file:
            if file.name.lower().endswith(".epub"):
                return file
            else:
                raise serializers.ValidationError(
                    "As of yet our API supports EPUB format only. Support for more formats will be added in the future."
                )
        return file

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["added_by"] = user
        print(validated_data)
        return super().create(validated_data)


class BookUserSerializer(BookSeriazlier):
    class Meta:
        model = Book
        exclude = ("added_by",)
