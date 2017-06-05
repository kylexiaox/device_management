from playhouse.pool import PooledMySQLDatabase

MAIL_SERVER='mail.migu.cn'
MAIL_PORT = 465
MAIL_USERNAME = 'xiaoxiang'
MAIL_PASSWORD = 'xiaobai3'
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_ASCII_ATTACHMENTS = True

database = PooledMySQLDatabase(
        database='device_info',  # string
        max_connections=32,
        passwd='123321',  # string
        user='root',  # string
        host='localhost',  # string
        port=3306,  # int,
        autocommit=False
)