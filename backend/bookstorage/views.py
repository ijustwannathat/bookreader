import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile
from ebooklib import epub
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.permissions import IsAuthor

from .models import Book
from .serializers import BookSeriazlier


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]

    # ah sorry didnt want to write viewsets so gotta copy paste, such a simple logic does not need routers anyways
    # TODO: write a viewset and set the router up
    def perform_create(self, serializer):
        file: InMemoryUploadedFile = self.request.FILES.get("file")
        if file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
                tmp_file.write(file.read())
                read_file = tmp_file.name
            book = epub.read_epub(read_file)

            title = book.get_metadata("DC", "title")[0][0]
            author = book.get_metadata("DC", "creator")[0][0]
            description = book.get_metadata("DC", "description")[0][0]
            language = book.get_metadata("DC", "language")[0][0]
            identifier = book.get_metadata("DC", "identifier")[0][0]
            format = file.name.split(".")[-1]
            serializer.save(
                title=title,
                author=author,
                description=description,
                language=language,
                identifier=identifier,
                format=format,
                added_by=self.request.user,
                file=file,
            )
        else:
            serializer.save(added_by=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]


