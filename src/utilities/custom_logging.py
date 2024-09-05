# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Custom logger using Loguru
@author <sreddy@simplifyvms.com>
"""

import logging
import sys
from pathlib import Path

from loguru import logger

from src.config.config import settings


class InterceptHandler(logging.Handler):
    """
    Interception handler
    """
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        """
        Emit
        :param record:
        :return:
        """
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(
            depth=depth,
            exception=record.exc_info).log(
            level,
            record.getMessage())




class consoleHandler(logging.Handler):
    """
    Interception handler
    """
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        """
        Emit
        :param record:
        :return:
        """
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(
            depth=depth,
            exception=record.exc_info).log(
            level,
            record.getMessage())


class CustomizeLogger:
    """
    Customize logger class
    """
    
    @classmethod
    def make_logger1(cls):
        """
        Make logger
        :return:
        """
        customize_logger = cls.customize_logging(
            settings.default.logging_filename,
            level=settings[settings.env].logging.loggers_default_level,
            msg_format=settings.default.logging_format,
        )
        return customize_logger

    @classmethod
    def customize_logging1(cls, filepath: Path, level: str, msg_format: str):
        """
        Customize logging
        :param filepath:
        :param level:
        :param msg_format:
        :return:
        """
        logger.remove()

        logger.add(str(filepath), level=level.upper(), format=msg_format)
        #logging.basicConfig(handlers=[InterceptHandler()], level=level)
        # logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        # for _log in ['uvicorn',
        #              'uvicorn.error',
        #              'fastapi'
        #              ]:
        #     _logger = logging.getLogger(_log)
        #     _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)


    @classmethod
    def make_logger(cls):
        """
        Make logger
        :return:
        """
        customize_logger = cls.customize_logging(
            level=settings[settings.env].logging.loggers_default_level,
            msg_format=settings[settings.env].logging.logging_format,

        )
        return customize_logger

    @classmethod
    def customize_logging(cls, level: str, msg_format: str):
        """
        Customize logging
        :param filepath:
        :param level:
        :param msg_format:
        :return:
        """
        logger.remove()
        logger.add(logging.StreamHandler(sys.stdout),level=level.upper(), format=msg_format)
        #logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=level)
        #logging.getLogger().addHandler(logging.StreamHander(sys.stdout))
        #logger.add(str(filepath), level=level.upper(), format=msg_format)
        #logging.basicConfig(handlers=[InterceptHandler()], level=0)
        # logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        # for _log in ['uvicorn',
        #              'uvicorn.error',
        #              'fastapi'
        #              ]:
        #     _logger = logging.getLogger(_log)
        #     _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        if CustomizeLogger._logger is None:
            CustomizeLogger._logger = CustomizeLogger.make_logger()
        
        return CustomizeLogger._logger
        pass
    
cust_logger = CustomizeLogger.get_logger()
