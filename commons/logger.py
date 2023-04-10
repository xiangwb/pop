#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    loggers
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    统一日志处理工具定义
    
    :author: leo
    :copyright: (c) 2020, Tungee
    :date created: 2020-04-29 17:02
 
"""
import json
import os
import logging
from logging import getLogger, Formatter
from logging.handlers import TimedRotatingFileHandler


class Logger(object):

    def __init__(self, **kwargs):
        self.api_logger = None

    def init_loggers(self, app):
        log_level = logging.DEBUG if app.config['DEBUG'] else logging.ERROR
        self.api_logger = get_logger(app, 'api_logger', log_level=log_level)
        # FIXME: 多个logger在这里继续进行定义


class FileFormatter(Formatter):
    """ For recording json format data log
    """

    def __init__(self):
        super(FileFormatter, self).__init__()

    def format(self, record):
        """ Override format function"""
        line = (
            '[{time}]|{level_name}|{pathname}|line:{line_no}|'
            '{function_name}|%s'
        ).format(
            time=self.formatTime(record, self.datefmt),
            level_name=record.levelname,
            pathname=record.pathname,
            line_no=record.lineno,
            function_name=record.funcName
        )
        if isinstance(record.msg, dict):
            s = line % json.dumps(record.msg, ensure_ascii=False)
            return s
        else:
            s = line % str(record.msg)
            return s


def get_file_logger(app, name=None, filename=None, when='midnight', interval=1, log_level=logging.DEBUG,
                    backup_count=20, notify=True, formatter_args=None):
    """ Get traceback logger
    :param app: app
    :param name: logger名称
    :param filename: logger输出文件名（只需要文件名，放在log目录下）
    :param when: 按时间保存的间隔单位
    :param interval: 保存间隔
    :param log_level: 日志打印等级，参考logging日志等级
    :param backup_count: 保存logger文件数量
    :param notify: 是否发送通知(级别为ERROR以上的需要发送短信和邮件通知)
    :param formatter_args: Formatter类参数
    """
    logger = getLogger(name) if name else getLogger(__name__)

    if not filename:
        filename = os.path.join(app.config['DEFAULT_LOG_DIR'], app.config['DEFAULT_LOG_FILE'])
    else:
        filename = os.path.join(app.config['DEFAULT_LOG_DIR'], filename)

    # 输出格式
    if formatter_args:
        formatter = Formatter(*formatter_args)
    else:
        formatter = FileFormatter()

    file_handler = TimedRotatingFileHandler(filename, when=when, interval=interval, backupCount=backup_count)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    # 报错邮件和短信
    if notify:
        # TODO：待完善
        pass

    return logger


def get_logger(app, name=None, log_level=logging.DEBUG, notify=True):
    """ Get traceback logger
    :param app: app
    :param name: logger名称
    :param log_level: 日志打印等级，参考logging日志等级
    :param notify: 是否发送通知(级别为ERROR以上的需要发送短信和邮件通知)
    """
    logger = getLogger(name) if name else getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s | [%(name)s:%(lineno)s]")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(console_handler)

    # 报错邮件和短信
    if notify:
        # TODO：待完善
        pass

    return logger
