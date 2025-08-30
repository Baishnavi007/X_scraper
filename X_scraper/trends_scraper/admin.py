from django.contrib import admin
from .models import TrendRun


@admin.register(TrendRun)
class TrendRunAdmin(admin.ModelAdmin):
    list_display = ("id", "scraped_at", "ip_address", "trend1", "trend2", "trend3", "trend4", "trend5")
    list_filter = ("scraped_at", "ip_address")
    search_fields = ("trend1", "trend2", "trend3", "trend4", "trend5", "ip_address")
    ordering = ("-scraped_at",)
