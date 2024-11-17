import fitz


def save_pdf_thumbnail(pdf_path: str, dest_path: str):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save(dest_path)

    doc.close()


def get_pdf_pages_count(pdf_path: str) -> int:
    doc = fitz.open(pdf_path)

    return doc.page_count
