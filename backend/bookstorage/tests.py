import os
import shutil
from collections import Counter

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.models import User, get_token_for_user

from .handlers import EpubHandler

path = "books/"


class TestBook(APITestCase):
    def setUp(self) -> None:
        email = "tomandjarry@gmail.com"
        password = "banish12345"
        d = reverse("token_obtain_pair")
        self.user_instance = User.objects.create_user(
            id=224, email=email, password=password
        )
        self.get_token = get_token_for_user(self.user_instance).get("refresh")
        self.user_instance.token = self.get_token
        self.user_instance.save()

        self.usr = self.client.post(d, {"email": email, "password": password})
        self.token = self.usr.json().get("access")
        self.test_files_path = os.path.join(settings.MEDIA_ROOT, "user_224")

    def upload_file(self, filepath: str, token: str):
        with open(filepath, "rb") as f:
            content = f.read()

        url = reverse("book-view")

        response = self.client.post(
            url,
            {
                "file": SimpleUploadedFile(
                    content=content,
                    name=os.path.basename(filepath),
                    content_type="epub+zip",
                ),
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        return response

    def test_file_uploads(self):
        files = os.listdir(path)
        for file in files:
            response = self.upload_file(filepath=path + file, token=self.token)
            print(response)

        else:
            print(
                "----------------------------------------------------------------------"
            )
        print(f"Run {len(files)} files. OK")

    def tearDown(self):
        try:
            shutil.rmtree(str(self.test_files_path))
        except OSError as e:
            print(e)
