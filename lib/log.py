"""
lib.log:
Framework for logging
"""
import logging

def warn(msg: str):
    logging.warning(msg)

def debug(msg: str):
    logging.debug(msg)

def info(msg: str):
    logging.info(msg)
