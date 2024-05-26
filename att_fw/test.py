import sys
from loguru import logger

# 添加控制台输出
logger.add(sink=sys.stdout, format="{time} {level} {message}", level="DEBUG")

# 添加文件输出
logger.add(sink="myapp.log", format="{time} {level} {message}", level="DEBUG")

# 输出日志
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')
logger.critical('This is a critical message')
