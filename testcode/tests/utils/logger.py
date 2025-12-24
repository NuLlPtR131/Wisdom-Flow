"""
测试日志配置模块

配置测试过程中的日志记录格式和输出方式。

作者：QA Team
创建日期：2025-01-16
版本：1.0
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_test_logger(log_level: str = "INFO", log_file: str = None):
    """
    配置测试日志记录器。
    
    Args:
        log_level: 日志级别，默认 "INFO"
        log_file: 日志文件路径，不提供则只输出到控制台
    """
    # 创建日志目录
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        # 默认日志文件路径
        log_dir = Path(__file__).parent.parent.parent / "test_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # 日志格式
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 配置根日志记录器
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        datefmt=date_format,
        handlers=[
            # 控制台处理器
            logging.StreamHandler(sys.stdout),
            # 文件处理器
            logging.FileHandler(log_file, encoding="utf-8"),
        ]
    )
    
    # 设置第三方库日志级别
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    
    logging.info(f"测试日志已配置，日志文件: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器。
    
    Args:
        name: 日志记录器名称
        
    Returns:
        logging.Logger: 日志记录器实例
    """
    return logging.getLogger(name)

