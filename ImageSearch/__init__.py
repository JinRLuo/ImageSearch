# import pymysql
from pymilvus import connections

# pymysql.install_as_MySQLdb()


# Connect to Milvus service
connections.connect(host="10.11.89.130", port="19530")


