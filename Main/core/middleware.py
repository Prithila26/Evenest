import logging
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, AnonymousUser
from django.db import close_old_connections

logger = logging.getLogger(__name__)

class WebSocketDebugMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        if scope["type"] == "websocket":
            logger.info(f"WebSocket {scope.get('client', ['Unknown'])[0]} connecting to {scope.get('path', 'Unknown path')}")
            
        modified_receive = self.receive_with_logging(receive)
        modified_send = self.send_with_logging(send)
        
        return await super().__call__(scope, modified_receive, modified_send)

    async def receive_with_logging(self, receive):
        message = await receive()
        if message["type"] == "websocket.connect":
            logger.info("WebSocket connection initiated")
        elif message["type"] == "websocket.disconnect":
            logger.info("WebSocket disconnection initiated")
        elif message["type"] == "websocket.receive":
            logger.info("WebSocket message received")
        return message

    async def send_with_logging(self, send):
        async def wrapped_send(message):
            if message["type"] == "websocket.accept":
                logger.info("WebSocket connection accepted")
            elif message["type"] == "websocket.close":
                logger.info("WebSocket connection closed")
            elif message["type"] == "websocket.send":
                logger.info("WebSocket message sent")
            await send(message)
        return wrapped_send

class WebSocketMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        try:
            # Close old database connections to prevent usage of timed out connections
            close_old_connections()

            # Get session from scope
            session_key = None
            if scope["type"] == "websocket":
                query_string = scope.get("query_string", b"").decode()
                if "session_key=" in query_string:
                    session_key = query_string.split("session_key=")[-1].split("&")[0]

            if not session_key:
                logger.warning("No session key found in WebSocket connection")
                scope['user'] = AnonymousUser()
                return await super().__call__(scope, receive, send)

            # Get user from session
            user = await self.get_user_from_session(session_key)
            scope['user'] = user if user else AnonymousUser()

            if not user:
                logger.warning(f"No user found for session key: {session_key}")

            return await super().__call__(scope, receive, send)
            
        except Exception as e:
            logger.error(f"Error in WebSocket middleware: {str(e)}")
            scope['user'] = AnonymousUser()
            return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user_from_session(self, session_key):
        try:
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')
            return User.objects.get(id=user_id)
        except (Session.DoesNotExist, User.DoesNotExist) as e:
            logger.error(f"Session/User lookup failed: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in get_user_from_session: {str(e)}")
            return None