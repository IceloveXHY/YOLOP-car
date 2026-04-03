# road_detection/routing.py
from django.urls import re_path
from road_detection import consumers

websocket_urlpatterns = [
    re_path(r'ws/process/(?P<task_id>[\w-]+)/$', consumers.VideoProcessingConsumer.as_asgi()),
]