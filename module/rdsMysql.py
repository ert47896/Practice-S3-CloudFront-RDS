from mysql.connector import pooling
import os
from dotenv import load_dotenv
load_dotenv()

connection_pool = pooling.MySQLConnectionPool(
    host = os.getenv("RDS_HOST"),
    port = os.getenv("PORT"),
    user = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD"),
    database = os.getenv("DATABASE"),
    pool_name = "mypool",
    pool_size = 5
)