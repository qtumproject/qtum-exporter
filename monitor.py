#!/usr/bin/env python3

from datetime import (
    datetime, timedelta
)
from prometheus_client import start_wsgi_server
from logging import (
    Logger, Formatter, StreamHandler
)
from signal import (
    signal, SIGTERM
)

import logging
import sys

from src.config import Config
from src.collector import collect
from src.metrics import (
    EXPORTER_ERRORS, PROCESS_TIME
)


def sigterm_handler(*args) -> None:
    logger.critical("Received SIGTERM. Exiting Qtum (qtumd) monitor.")
    sys.exit(0)


def exception_count(exception: Exception) -> None:
    err_type = type(exception)
    exception_name = err_type.__module__ + "." + err_type.__name__
    EXPORTER_ERRORS.labels(**{"type": exception_name}).inc()


if __name__ == "__main__":
    # Set up logging to look similar to qtum logs (UTC).
    logger: Logger = logging.getLogger(f"qtum-exporter-monitor")
    logger.setLevel(level=Config.LOGGING_LEVEL)
    formatter: Formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    stream_handler: StreamHandler = logging.StreamHandler()
    stream_handler.setFormatter(fmt=formatter)
    logger.addHandler(stream_handler)

    # Handle SIGTERM gracefully.
    signal(SIGTERM, sigterm_handler)
    logger.info("Started Qtum (qtumd) monitor.")

    start_wsgi_server(
        port=Config.METRICS_PORT, addr=Config.METRICS_ADDRESS
    )

    try:
        last_refresh: datetime = (
            datetime.now() - timedelta(seconds=Config.REFRESH_SECONDS)
        )
        while True:
            process_start: datetime = datetime.now()
            # Only refresh every REFRESH_SECONDS seconds.
            if (process_start - last_refresh).total_seconds() < Config.REFRESH_SECONDS:
                continue

            try:
                collect()
            except Exception as exception:
                logger.error(f"Exception: {str(exception)}", exc_info=True)
                exception_count(exception)

            duration = datetime.now() - process_start
            PROCESS_TIME.inc(duration.total_seconds())
            logger.info("Refresh took %s seconds", duration.total_seconds())
            last_refresh = process_start
    except KeyboardInterrupt:
        logger.critical("Exiting Qtum (qtumd) monitor.")
        sys.exit(0)
