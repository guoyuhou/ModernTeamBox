from django.urls import re_path

def get_websocket_urlpatterns():
    from . import consumers  # 将这个导入移到函数内部
    return [
        re_path(r'ws/game/(?P<game_id>\w+)/$', consumers.GameConsumer.as_asgi()),
        re_path(r'ws/lobby/$', consumers.LobbyConsumer.as_asgi()),
    ]

websocket_urlpatterns = get_websocket_urlpatterns()
