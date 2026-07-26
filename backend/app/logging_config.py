import logging
import time

from flask import g, request
from werkzeug.exceptions import HTTPException


def configure_logging(app):
    """Structured request logging + a safety-net handler for unexpected errors.

    Logs to stdout rather than a file: on Render/Docker the container's
    stdout is already captured by the platform's log viewer, and a log file
    inside the container would just be lost on every restart anyway.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s"))
    app.logger.handlers = [handler]
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)

    @app.before_request
    def _start_timer():
        g._request_start_time = time.time()

    @app.after_request
    def _log_request(response):
        duration_ms = (time.time() - g.get("_request_start_time", time.time())) * 1000
        app.logger.info("%s %s -> %s (%.1fms)", request.method, request.path, response.status_code, duration_ms)
        return response

    @app.errorhandler(Exception)
    def _handle_unexpected_error(exc):
        if isinstance(exc, HTTPException):
            return exc
        app.logger.exception("Unhandled exception on %s %s", request.method, request.path)
        return {"error": "An unexpected error occurred. Please try again."}, 500
