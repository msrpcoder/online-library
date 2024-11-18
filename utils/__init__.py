import fitz

from activity.models import Activity


def save_pdf_thumbnail(pdf_path: str, dest_path: str):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    pix.save(dest_path)

    doc.close()


def get_pdf_pages_count(pdf_path: str) -> int:
    doc = fitz.open(pdf_path)

    return doc.page_count


def log_activity(actor, activity_type, description, object_details=None):
    activity = Activity()
    activity.actor = actor
    activity.activity_type = activity_type
    activity.description = description
    activity.object_details = object_details

    activity.save()

    return activity
