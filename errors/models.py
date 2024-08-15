from django.db import models
from django.conf import settings

class ErrorMessage(models.Model):
    title = models.CharField(max_length=200)
    error_message = models.TextField()
    steps_to_reproduce = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
