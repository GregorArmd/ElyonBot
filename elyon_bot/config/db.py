import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')

connection = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_pass,
    database=db_name,
)

cursor = connection.cursor()

# connection.close()