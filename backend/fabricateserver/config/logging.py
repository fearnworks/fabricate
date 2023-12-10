from rich.console import Console
from rich.logging import RichHandler
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from loguru import logger 
# Create a console instance
console = Console()

logger.remove()
logger.add(RichHandler())

class LogMiddleware(BaseHTTPMiddleware):
    """ Middleware to log all incoming requests. """
    async def dispatch(self, request: Request, call_next):
        """ Log all incoming requests. """
        if hasattr(request.state, "body"):
            body_json = request.state.body
        else:
            body_json = None
        logger.info(f"Incoming request: {request.method} {request.url} {body_json}")
        response = await call_next(request)
        return response
