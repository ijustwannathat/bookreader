from django.db import models


def user_directory_path(instance, filename):
    return f"user_{instance.added_by.id}/{filename}"


class Book(models.Model):
    title = models.CharField(max_length=700)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=5, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(blank=True, null=True)
    format = models.CharField(max_length=12)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True)
    added_by = models.ForeignKey(
        "accounts.User", related_name="books", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.title}. by {self.author}"

