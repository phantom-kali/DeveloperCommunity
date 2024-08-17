from django.contrib import admin
from .models import Vote, Report

class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'object_id', 'vote')
    list_filter = ('content_type', 'vote')
    search_fields = ('user__username', 'content_type__model', 'object_id')

class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_by', 'content_type', 'object_id', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('reported_by__username', 'content_type__model', 'object_id', 'reason')
    readonly_fields = ('created_at',)

admin.site.register(Vote, VoteAdmin)
admin.site.register(Report, ReportAdmin)
