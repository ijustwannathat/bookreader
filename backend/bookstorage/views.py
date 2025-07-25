import pprint

from ebooklib.epub import EpubException
from rest_framework import generics
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import Response

from accounts.permissions import IsAuthor

from .models import Book
from .serializers import BookDetailSerializer, BookSeriazlier


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSeriazlier
    # temporary measure that as i thought would work for basic logic, i didnt focus on writing permissions explicitly
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user

        return (
            super().get_queryset()
            if user.is_staff
            else super().get_queryset().filter(added_by=user.id)
        )

    def post(self, request, *args, **kwargs):
        try:

            data = super().post(request, *args, **kwargs)
            return data
        except EpubException as e:
            return Response(
                {
                    "Error": "During filehandling an error occured, the file may be corrupted. "
                    + "Try reinstalling the file, because it might've gotten damage during downloading. "
                    + "Try converting to other formats if it didn't help or try contacting us directly.",
                    "Error message": e.with_traceback(None).msg,
                }
            )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    # i have no fucking clue why IsAuthor permission works here
    permission_classes = [IsAuthor]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        # pprint.pprint(self.__dict__)
        return super().get(request, *args, **kwargs)
