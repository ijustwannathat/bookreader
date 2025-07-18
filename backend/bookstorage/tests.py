from django.test import TestCase
from bookstorage.models import Book
import os
from ebooklib import epub

path = '/home/yuriypazirovych/Documents/Books/Development/Django/progit.epub'


class TestBook(TestCase):
    def test_file_upload(self):
        book_file = Book.objects.create(title='progit',author='George', format='epub', file=path) 
        book_file.save()
        print(book_file.file)



