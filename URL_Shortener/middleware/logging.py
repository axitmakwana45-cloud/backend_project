import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        request_id = getattr(request.state, "request_id", "N/A")
        logger.info(
            "%s %s %s %.4f sec",
            request.method,
            request.url.path,
            request_id,
            response.status_code,
            process_time,
        )

        return response