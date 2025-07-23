import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User, get_token_for_user


class TestBook(APITestCase):
    def setUp(self) -> None:
        email = "tomandjarry@gmail.com"
        password = "banish12345"
        d = "http://127.0.0.1:8000/api/token/"
        self.user_instance = User.objects.create_user(
            id=224, email=email, password=password
        )
        self.get_token = get_token_for_user(self.user_instance).get("refresh")
        self.user_instance.token = self.get_token
        self.user_instance.save()

        self.usr = self.client.post(d, {"email": email, "password": password})
        self.token = self.usr.json().get("access")

    def upload_file(self, filepath: str, token: str):
        with open(filepath, "rb") as f:
            content = f.read()
            url = reverse("book-view")

            response = self.client.post(
                url,
                {
                    "file": SimpleUploadedFile(
                        content=content,
                        name=os.path.basename(path),
                        content_type="epub+zip",
                    ),
                    "title": "1",
                    "author": "1",
                    "format": "epub",
                },
                headers={"Authorization": f"Bearer {token}"},
            )
            return response

    def test_file_upload(self):
        result = self.upload_file(filepath=path, token=self.token)
        print(result)
