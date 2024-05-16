#!/usr/bin/env python3
"""filter_datum returns the log message obfuscated"""
import re


def filter_datum(fields, redaction, message, separator):
    """filter_datum returns the log message obfuscated"""
    return re.sub(rf'({"|".join(fields)})=[^{separator}]*',
                  lambda m: f"{m.group().split('=')[0]}={redaction}", message)
