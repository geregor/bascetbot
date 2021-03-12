import pymysql.cursors
from boto.s3.connection import S3Connection
import os

def connect():
    connection = pymysql.connect(
        host='remotemysql.com',
        user='VcJhVl8VY9',
        password='2szV2WF4BO',
        db='VcJhVl8VY9',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

# Тир 1 - 1-7
# Тир 2 - 8-15
# Тир 3 - 16-25
# Тир 4 - 26 - ...
