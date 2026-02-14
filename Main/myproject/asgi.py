"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from core.routing import websocket_urlpatterns
from core.middleware import WebSocketMiddleware, WebSocketDebugMiddleware
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            WebSocketDebugMiddleware(
                WebSocketMiddleware(
                    URLRouter(
                        websocket_urlpatterns
                    )
                )
            )
        )
    ),
})
