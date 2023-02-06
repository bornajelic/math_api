import logging
import random
import string
import sys
import time

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from math_api.utils.settings import api_config


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class CustomizeLogger:
    @classmethod
    def make_logger(cls):
        logger = cls.customize_logging(
            level=api_config.LOG_LEVEL,
            format=api_config.FORMAT,
            json_logs=api_config.JSON_LOGS,
        )
        return logger

    @classmethod
    def customize_logging(
        cls,
        level: str,
        format: str,
        json_logs: int,
    ):
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=level.upper(),
            format=format,
            serialize=json_logs,
        )

        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


class CustomLogTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        start_time = time.time()
        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = "{0:.2f}".format(process_time)

        logger.info(
            f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
        )

        return response
