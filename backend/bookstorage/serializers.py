from rest_framework import serializers

from .handlers import EpubHandler
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
        file = validated_data.get("file")
        if file:
            instance = EpubHandler(file=file)
            handled_data = instance.handle_file()
            validated_data.update(handled_data)

        return super().create(validated_data)


class BookUserSerializer(BookSeriazlier):
    class Meta:
        model = Book
        exclude = ("added_by",)
