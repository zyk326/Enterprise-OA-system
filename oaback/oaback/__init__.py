# 添加数据库启动
import pymysql
pymysql.install_as_MySQLdb()

# 添加celery启动
from .celery import app as celery_app
__all__ = ("celery_app", )