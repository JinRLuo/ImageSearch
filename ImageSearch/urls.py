"""ImageSearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.urls import path
from . import views, settings

urlpatterns = [
    path('index/', views.index, name='index'),
    path('word_search_image', views.word_search_image, name='word_search_image'),
    path('image_search_image', views.image_search_image, name='image_search_image'),
    path('image_zt_tag', views.image_zt_tag, name='image_zt_tag'),
    path('upload_images', views.upload_images, name='upload_images')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
