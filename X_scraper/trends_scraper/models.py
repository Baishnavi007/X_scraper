from django.db import models
import uuid


class TrendRun(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    trend1 = models.CharField(max_length=255, blank=True, null=True)
    trend2 = models.CharField(max_length=255, blank=True, null=True)
    trend3 = models.CharField(max_length=255, blank=True, null=True)
    trend4 = models.CharField(max_length=255, blank=True, null=True)
    trend5 = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scraped_at"]  # ✅ latest() queries safe + predictable

    def __str__(self):
        return f"TrendRun {self.id} at {self.scraped_at}"
