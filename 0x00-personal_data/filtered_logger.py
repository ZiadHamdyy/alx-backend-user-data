#!/usr/bin/env python3
"""filter_datum returns the log message obfuscated"""
import re
from typing import List, Tuple
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """filter_datum returns the log message obfuscated"""
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*',
                  lambda m: f"{m.group().split('=')[0]}={redaction}", message)


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with specified fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record, redacting specified fields."""
        original_message = super(RedactingFormatter, self).format(record)
        redacted_message = filter_datum(self.fields, self.REDACTION,
                                        original_message, self.SEPARATOR)
        return redacted_message


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger to log user data with
    sensitive information redacted.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
