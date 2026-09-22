from django.db import models


class MuscleGroup(models.Model):
    """Class representing a Muscle Group table."""
    class Meta:
        ordering = ["name"]
        db_table = "muscle_group"
        verbose_name = "Muscle Group"
        verbose_name_plural = "Muscle Groups"

    name = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
