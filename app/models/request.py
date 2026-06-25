from fastapi import UploadFile


class InvoiceRequest:
    def __init__(self, file: UploadFile):
        self.file = file
