from django.test import TestCase


from .models import User


class UserTest(TestCase):
    def test_user(self):
        usr = User.objects.create(email="kokfbc1@gmail.com", password="pazirovish")
        usr.save()

        print(usr.password)
