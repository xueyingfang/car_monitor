import logging
import os
from logging.handlers import RotatingFileHandler

class LogUtil:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_log()
        return cls._instance

    def _init_log(self):
        """初始化日志：同时输出控制台 + 滚动日志文件 monitor.log"""
        log_file = "monitor.log"
        self.logger = logging.getLogger("CarMonitor")
        self.logger.setLevel(logging.INFO)
        # 防止重复添加handler
        if self.logger.handlers:
            return

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # 文件输出：单个文件最大5M，最多保留3个备份
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


# 全局单例实例，外部直接导入使用
log = LogUtil()
