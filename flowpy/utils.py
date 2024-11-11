import logging
import logging.handlers

LOG = logging.getLogger(__name__)
__all__ = ("setup_logging",)


def setup_logging(*, formatter: logging.Formatter | None = None) -> None:
    level = logging.DEBUG

    handler = logging.handlers.RotatingFileHandler(
        "flowpy.log", maxBytes=1000000, encoding="UTF-8"
    )

    if formatter is None:
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(
            "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
        )

    logger = logging.getLogger()
    handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(handler)
