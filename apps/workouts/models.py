from django.db import models


class Workout(models.Model):
    """Class representing a Workout table."""
    class Meta:
        verbose_name_plural = "workouts"
        db_table = "workout"
        ordering = ["-date"]

    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Workout on {self.date}"


class WorkoutExercise(models.Model):
    """Class representing a WorkoutExercise table."""
    class Meta:
        verbose_name_plural = "workout exercises"
        db_table = "workout_exercise"
        ordering = ["id"]

    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=100)
    volume = models.CharField(max_length=255)
    rest = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exercise_name} in {self.workout}"


class WorkoutSet(models.Model):
    """Class representing a WorkoutSet table."""
    class Meta:
        verbose_name_plural = "workout sets"
        db_table = "workout_set"
        ordering = ["id"]

    workout_exercise = models.ForeignKey(
        WorkoutExercise, on_delete=models.CASCADE, related_name='workout_sets')
    set_number = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Set {self.set_number} of {self.workout_exercise}"
