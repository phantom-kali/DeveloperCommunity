from django.db import models
from django.conf import settings

class CodeSnippet(models.Model):
    title = models.CharField(max_length=200)
    code = models.TextField()
    language = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
