import tempfile

from django.test.client import BaseHandler
from ebooklib import epub

# does not work here properly, throws str has no attribute read()
# does work in views.py tho, bad solution anyways cause tests are needed and maybe it would be better to write that 
# in models.py for better test cases, i foresee that the above mentioned error may cause problems
#TODO: expand range of cases it can handle (would be cool to add byte handler and str handler for path)

class EpubHandler(BaseHandler):
    def __init__(self, file) -> None:
        # it accepts only
        # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'> type

        self.file = file

    def handle_file(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as tmp_file:
            tmp_file.write(self.file.read())
            read_file = tmp_file.name
        book = epub.read_epub(read_file)

        # i think maybe we need to make it into sum([]), cuz sometimes file is not being handled properly
        # since not all elements are nested inside the array
        #TODO: make a sense out of it, also write a custom function that generates a random hash for a filename
        # in case file name is not determined
        title = book.get_metadata("DC", "title")[0][0]
        author = book.get_metadata("DC", "creator")[0][0]
        description = book.get_metadata("DC", "description")[0][0]
        language = book.get_metadata("DC", "language")[0][0]
        identifier = book.get_metadata("DC", "identifier")[0][0]
        format = self.file.name.split(".")[-1]
        metadata = {
                'title': title,
                'author': author,
                'description': description,
                'language' : language,
                'identifier': identifier,
                'format': format
                }
        return metadata




