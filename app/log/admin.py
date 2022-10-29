from django.contrib import admin

from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "start", "end", "message"]
    list_filter = ("name",)
    ordering = ("-start",)