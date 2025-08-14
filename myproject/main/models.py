# main/models.py
from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.IntegerField()  # Оценка 1–10
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.rating}/10"
