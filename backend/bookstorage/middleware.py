import magic


class FiletypeHandlerMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response
        # allowed formats are things this middleware will handle, i will probably write them in here
        # and after testing them for a little create a dedicated class for each of them
        # im just tipping my toes into the water to see what does this thing do
        self.allowed_formats = ["epub", "pdf", "mobi", "azw3"]

    def __call__(self, request):
        if request.method == "POST" and "file" in request.FILES:
            uploaded_file = request.FILES["file"]

            mime = magic.Magic(mime=True)

            btrc = uploaded_file.read(2048)
            print(mime.from_buffer(btrc))
            uploaded_file.seek(0)

        response = self.get_response(request)

        return response
