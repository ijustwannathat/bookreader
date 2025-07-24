from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser

from accounts.permissions import IsAuthor

from .handlers import EpubHandler
from .models import Book
from .serializers import BookSeriazlier


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    # temporary measure that as i thought would work for basic logic, i didnt focus on writing permissions explicitly
    # permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        data = super().post(request, *args, **kwargs)
        print(data.data)
        return data

    # TOFIX: with planned filtering and stuff this shit definitely needs a router
    # def perform_create(self, serializer):
    # file = self.request.FILES.get("file")
    #
    # if file:
    #     instance = EpubHandler(file=file)
    #     handled_data = instance.handle_file()
    #     serializer.save(**handled_data)
    # else:
    # serializer.save(added_by=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]
