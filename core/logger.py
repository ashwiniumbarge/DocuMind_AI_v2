"""
============================================================
DocuMind AI v2
Logging Module
============================================================
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import LOG_FILE, LOG_LEVEL


class Logger:

    _logger = None

    @staticmethod
    def get_logger(name: str = "DocuMindAI"):

        if Logger._logger:
            return Logger._logger

        logger = logging.getLogger(name)

        logger.setLevel(getattr(logging, LOG_LEVEL.upper()))

        if logger.handlers:
            return logger

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # -------------------------
        # Console Handler
        # -------------------------

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # -------------------------
        # File Handler
        # -------------------------

        Path(LOG_FILE).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        logger.propagate = False

        Logger._logger = logger

        return logger


logger = Logger.get_logger()