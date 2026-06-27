from io import BytesIO

import easyocr
import numpy as np
from PIL import Image

from app.utils.pdf import pdf_to_images


class OCRService:
    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)

    def extract_text(self, file_bytes: bytes, filename: str) -> str:
        if filename.lower().endswith(".pdf"):
            return self._ocr_pdf(file_bytes)
        return self._ocr_image(file_bytes)

    def _ocr_pdf(self, file_bytes: bytes) -> str:
        images = pdf_to_images(file_bytes)
        text_parts = []
        for img in images:
            arr = np.array(img)
            result = self.reader.readtext(arr)
            text_parts.append(self._parse_result(result))
        return "\n".join(text_parts)

    def _ocr_image(self, file_bytes: bytes) -> str:
        img = Image.open(BytesIO(file_bytes))
        arr = np.array(img)
        result = self.reader.readtext(arr)
        return self._parse_result(result)

    def _parse_result(self, result) -> str:
        return "\n".join(item[1] for item in result)
