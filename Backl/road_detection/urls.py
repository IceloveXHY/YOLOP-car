"""
URL configuration for road_detection project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django import views
from django.contrib import admin
from django.urls import path, re_path
from app01.views import drowsy_driving, upload_video, lane_markings, throws
from app01.views import index
from django.conf import settings
from django.conf.urls.static import static

from road_detection import consumers

urlpatterns = [
    path('',index, name='index'),
    path('admin/', admin.site.urls),
    path('drowsy_driving/', drowsy_driving, name='drowsy_driving'),
    # path('illegal_parking/', illegal_parking, name='illegal_parking'),
    path('api/upload', upload_video),
    path('lane_markings/', lane_markings, name='lane_markings'),
    path('throws/', throws, name='throws'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # 开发环境下的媒体文件路由
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
