# import pymysql
from pymilvus import connections

# pymysql.install_as_MySQLdb()


# Connect to Milvus service

connections.connect(host="db", port="19530")


