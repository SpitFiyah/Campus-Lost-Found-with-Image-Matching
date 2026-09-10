from pathlib import Path
from uuid import uuid4

from PIL import Image, UnidentifiedImageError
from werkzeug.datastructures import FileStorage


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
ALLOWED_IMAGE_MIMETYPES = {"image/jpeg", "image/png", "image/webp"}


def save_validated_image(file_storage: FileStorage, upload_folder: str):
    if not file_storage or not file_storage.filename:
        return None, ("IMAGE_REQUIRED", "At least one image is required.")
    extension = Path(file_storage.filename).suffix.lower().lstrip(".")
    if extension not in ALLOWED_IMAGE_EXTENSIONS or file_storage.mimetype not in ALLOWED_IMAGE_MIMETYPES:
        return None, ("INVALID_IMAGE", "Only JPG, PNG, and WEBP images are supported.")

    try:
        image = Image.open(file_storage.stream)
        image.verify()
        file_storage.stream.seek(0)
    except (UnidentifiedImageError, OSError):
        return None, ("INVALID_IMAGE", "The uploaded file is not a valid image.")

    safe_name = f"{uuid4().hex}.{extension}"
    upload_path = Path(upload_folder)
    upload_path.mkdir(parents=True, exist_ok=True)
    destination = upload_path / safe_name
    file_storage.save(destination)
    return safe_name, None
