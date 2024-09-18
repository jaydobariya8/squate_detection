from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('camera/', views.camera_view, name='camera'),
    path('save-image/', views.save_image, name='save_image'),
]
