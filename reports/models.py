from django.db import models

class DrowsinessReport(models.Model):
    mac_address = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    dni = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    vehicle_type = models.CharField(max_length=100)
    plate = models.CharField(max_length=20)
    blink_count = models.IntegerField()
    yawn_count = models.IntegerField()
    nod_count = models.IntegerField()
    critical_events = models.JSONField()
    video_names = models.JSONField()
    url_videos = models.JSONField(default=list)
    generated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(max_length=20, default="No revisado")
    gravedad = models.CharField(max_length=20, default="Desconocida")

    def __str__(self):
        return f"Reporte de {self.first_name} {self.last_name} - {self.generated_at}"
