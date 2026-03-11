from channels.routing import URLRouter
from chat.routing import websocket_urlpatterns

application = URLRouter(websocket_urlpatterns)