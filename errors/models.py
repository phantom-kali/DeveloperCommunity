from django.db import models
from django.conf import settings

class ErrorMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    error_message = models.TextField()
    steps_to_reproduce = models.TextField()
    expected_behavior = models.TextField()
    actual_behavior = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pending_moderation = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Solution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    error_message = models.ForeignKey(ErrorMessage, on_delete=models.CASCADE, related_name='solutions')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Solution for {self.error_message.title}"