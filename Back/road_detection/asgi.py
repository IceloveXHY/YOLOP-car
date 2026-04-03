import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from road_detection import routing  # 假设这里存放 WebSocket 路由

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'road_detection.settings')

# 先获取 Django 的 HTTP 应用
http_application = get_asgi_application()

# 配置 ProtocolTypeRouter，区分 HTTP 和 WebSocket 请求
application = ProtocolTypeRouter({
    "http": http_application,  # 处理所有 HTTP 请求（包括 Django 原生路由）
    "websocket": URLRouter(
        routing.websocket_urlpatterns  # 处理所有 WebSocket 请求
    ),
})