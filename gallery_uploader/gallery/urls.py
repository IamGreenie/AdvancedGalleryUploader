from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from gallery.views import ImageCreateView, ImageListView, ImageDetailView, ViewingHistoryView, PersonalGalleryView

urlpatterns = [
    path('', ImageCreateView.as_view(), name='upload'),
    path('list/', ImageListView.as_view(), name='image-list'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image-detail'),
    path('history/', ViewingHistoryView.as_view(), name='viewing-history'),
    path('my-gallery/', PersonalGalleryView.as_view(), name='personal-gallery'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)