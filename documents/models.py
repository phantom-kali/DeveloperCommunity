from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
import magic
import os
from django.utils.crypto import get_random_string


def validate_file_type(file):
    allowed_types = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "text/plain",
    ]

    # Check MIME type
    file_mime = magic.from_buffer(file.read(1024), mime=True)
    if file_mime not in allowed_types:
        raise ValidationError(
            "Only PDF, Word documents, PowerPoint presentations, and text files are allowed."
        )

    # Reset file pointer
    file.seek(0)


def validate_file_size(value):
    filesize = value.size
    if filesize > 10 * 1024 * 1024:  # 10MB limit
        raise ValidationError("The maximum file size that can be uploaded is 10MB")


def get_unique_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{get_random_string(10)}.{ext}"
    return os.path.join("documents", filename)


class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to=get_unique_filename, validators=[validate_file_size, validate_file_type])
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EducationalLink(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    url = models.URLField(unique=True)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
