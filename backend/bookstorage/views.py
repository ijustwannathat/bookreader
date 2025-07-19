from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.permissions import IsAuthor

from .handlers import EpubHandler
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
        file = self.request.FILES.get("file")

        if file:
            instance = EpubHandler(file=file)
            handled_data = instance.handle_file()
            serializer.save(**handled_data)
        else:
            serializer.save(added_by=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]
