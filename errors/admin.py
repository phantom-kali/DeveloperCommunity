from django.contrib import admin
from .models import ErrorMessage, Solution

class ErrorMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'is_pending_moderation')
    list_filter = ('is_pending_moderation',)
    actions = ['approve_errors']

    def approve_errors(self, request, queryset):
        queryset.update(is_pending_moderation=False)
    approve_errors.short_description = "Approve selected errors"

admin.site.register(ErrorMessage, ErrorMessageAdmin)
admin.site.register(Solution)