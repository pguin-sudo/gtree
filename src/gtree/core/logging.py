import logging
import sys

import structlog
from structlog.stdlib import ProcessorFormatter


def setup_logging(level: str = "INFO") -> None:
    """Configures structlog + stdlib"""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    # Shared processors for foreign (stdlib) logs
    pre_chain = [
        # Add log level and timestamp if missing
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            # These run on structlog logs only
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Last: wrap for ProcessorFormatter
            ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Final formatter: applies to all logs (structlog + foreign)
    formatter = ProcessorFormatter(
        foreign_pre_chain=pre_chain,
        processors=[
            # Clean up ProcessorFormatter's meta keys (_record, etc.)
            ProcessorFormatter.remove_processors_meta,
            # Render as JSON (sort_keys for consistency)
            structlog.processors.JSONRenderer(sort_keys=True),
        ],
    )

    # Set up root logger
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper()))

    # logging.getLogger("uvicorn.access").disabled = True
