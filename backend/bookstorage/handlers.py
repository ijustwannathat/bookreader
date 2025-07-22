import hashlib
import random
import re
import tempfile

import magic
from django.test.client import BaseHandler
from ebooklib import epub
from ebooklib.epub import EpubBook


# im gonna rewrite that someday i promise
class EpubHandler(BaseHandler):
    def __init__(self, file) -> None:
        # it accepts only
        # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'> type

        self.file = file

    def generate_field_hash(self, field):
        """
        Sometimes file may not have name, therefore for easier identification we provide them with the filehash
        """
        bytes_encoded_string = (str(field) + str(random.randint(1, 300))).encode(
            "utf-8"
        )
        hash_encoded = hashlib.sha256(bytes_encoded_string)
        return hash_encoded.hexdigest()

    # I will rewrite that shit i promise
    # It will fail like the roman empire did
    def get_unsliced_or_none(self, data: list) -> str | int | None:
        """
        Epub get_metadata returns data in somewhat similar way
        !!!
        NOTE: Do not use this code if you're NOT handling EpubBook instance with .get_metadata method
        !!!
        magicwords = [("title"), {}]
        output = get_unsliced_or_none(magicwords)
        print(output) # output: title

        """
        if not data:
            return
        if isinstance(data, (str, int)):
            return data
        else:
            return self.get_unsliced_or_none(data[0])

    def get_epub_field(
        self,
        instance: EpubBook,
        field: str,
        namespace: str = "DC",
        set_default=False,
        default_hasher=hash,
    ) -> str | int | None:

        epub_field = self.get_unsliced_or_none(instance.get_metadata(namespace, field))

        if set_default:
            _default = default_hasher(field)
        else:
            _default = None
        return epub_field or _default

    # junk
    def get_filextension(self, file):
        mime = magic.Magic(mime=True)
        extension: str = file.name.split(".")[-1]
        file.seek(0)
        full_filetype: str = mime.from_buffer(file.read(2048))
        # simplified entries are ["application", 'filetype', 'addition']
        filetype = re.split(r"[/ | + | -]", full_filetype)[1]
        # i dont know why
        return {True: "epub"}.get("epub" in (filetype, extension))

    def handle_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
            tmp_file.write(self.file.read())
            read_file = tmp_file.name

        book = epub.read_epub(read_file)

        title = self.get_epub_field(
            book,
            namespace="DC",
            field="title",
            set_default=True,
            default_hasher=self.generate_field_hash,
        )
        author = self.get_epub_field(
            book,
            namespace="DC",
            field="creator",
        )
        description = self.get_epub_field(
            book,
            namespace="DC",
            field="description",
        )
        language = self.get_epub_field(
            book,
            namespace="DC",
            field="language",
        )
        identifier = self.get_epub_field(
            book,
            namespace="DC",
            field="identifier",
        )
        format = self.get_filextension(self.file)

        metadata = {
            "title": title,
            "author": author,
            "description": description,
            "language": language,
            "identifier": identifier,
            "format": format,
            "rating": 5,
        }

        return metadata
