import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gobang.settings')

def get_application():
    django_asgi_app = get_asgi_application()
    from game import routings  # 将这个导入移到函数内部
    return ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                routings.websocket_urlpatterns
            )
        ),
    })

application = get_application()
