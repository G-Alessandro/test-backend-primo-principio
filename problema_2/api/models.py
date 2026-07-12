from django.db import models


class StoricoEventi(models.Model):
    doy = models.IntegerField()
    event_index = models.IntegerField()
    x_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doy", "event_index"],
                name="vincolo_eventi"
            )
        ]
