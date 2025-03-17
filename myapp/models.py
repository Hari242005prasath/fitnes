from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Streak(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.count}"

class userDetails(models.Model):
    user=models.CharField(max_length=50)
    password=models.CharField(max_length=50)


class Gptinfo(models.Model):
    pdf_file = models.FileField(upload_to='fitness_plans/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Fitness Plan - {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-created_at']

class WorkoutStreak(models.Model):
    date = models.DateField(default=timezone.now)
    workout_type = models.CharField(max_length=100)
    duration = models.IntegerField()
    calories = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']
        # Ensure only one workout per day
        unique_together = ['date']

    def save(self, *args, **kwargs):
        # Update streak when saving
        super().save(*args, **kwargs)

class WorkoutAnalytics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    total_workouts = models.IntegerField(default=0)
    last_updated = models.DateField(auto_now=True)
