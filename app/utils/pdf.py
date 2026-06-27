import pypdfium2 as pdfium
from PIL import Image


def pdf_to_images(file_bytes: bytes, dpi: int = 200) -> list[Image.Image]:
    pdf = pdfium.PdfDocument(file_bytes)
    images = []
    for i in range(len(pdf)):
        page = pdf[i]
        bitmap = page.render(scale=dpi / 72)
        pil_image = bitmap.to_pil()
        images.append(pil_image)
    return images
