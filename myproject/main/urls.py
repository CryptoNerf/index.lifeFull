from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.mood_grid, name='mood_grid'),
    path('register/', views.register, name='register'),
    path('day/<str:day>/', views.edit_day, name='edit_day'),
    path('account/', views.account, name='account'),
    path('what_is_index/', views.what_is_index, name='what_is_index'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
