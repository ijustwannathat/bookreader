from rest_framework import serializers

from .handlers import EpubHandler
from .models import Book


class BookSeriazlier(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = [
            "title",
            "author",
            "description",
            "language",
            "identifier",
            "date_added",
            "rating",
            "added_by",
            "format",
        ]

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

        # logic is now handled by serializers since it may be easier to test import
        # also views are now do views stuff(maybe)
        if file:
            instance = EpubHandler(file=file, user_instance=user)
            handled_data = instance.handle_file()
            validated_data.update(handled_data)

        return super().create(validated_data)


class BookUserSerializer(BookSeriazlier):
    class Meta:
        model = Book
        exclude = ("added_by",)
