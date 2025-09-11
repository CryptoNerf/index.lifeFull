# main/models.py
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    rating = models.IntegerField()  # Оценка 1–10
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.date} - {self.rating}/10"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def save(self, *args, **kwargs):
        # Если это обновление существующего профиля
        if self.pk:
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                # Если старая фотка существует и новая фотка отличается от старой
                if old_profile.photo and old_profile.photo != self.photo:
                    # Удаляем старый файл с диска
                    if os.path.isfile(old_profile.photo.path):
                        os.remove(old_profile.photo.path)
            except Profile.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Удаляем файл фото при удалении профиля
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)

# Automatically create or update Profile when User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()