from django.contrib import admin
from .models import MoodEntry, Profile

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'date', 'rating', 'get_short_note']
    list_filter = ['rating', 'date', 'user']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'note']
    ordering = ['-date']
    date_hierarchy = 'date'
    list_per_page = 25
    
    def get_username(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        if full_name:
            return f"{obj.user.username} ({full_name})"
        return obj.user.username
    get_username.short_description = 'Пользователь'
    
    def get_short_note(self, obj):
        if not obj.note:
            return "Без заметки"
        return obj.note[:50] + "..." if len(obj.note) > 50 else obj.note
    get_short_note.short_description = 'Заметка'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'get_email', 'has_photo']
    search_fields = ['user__username', 'user__email']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Пользователь'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def has_photo(self, obj):
        return bool(obj.photo)
    has_photo.boolean = True
    has_photo.short_description = 'Есть фото'