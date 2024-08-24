import pymysql.cursors
import json


#Host: sql7.freesqldatabase.com
#Database name: sql7713987
#Database user: sql7713987
#Database password: 6H53PVXQWp
#Port number: 3306

# Чтение значений из внешнего JSON файла
with open('config.json') as json_file:
    data = json.load(json_file)
    host = data['host']
    port = data['port']
    user = data['user']
    password = data['password']
    database = data['database']

try:
    connection = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
    print("Подключение успешно установлено.")
except pymysql.Error as e:
    print(f"Ошибка при подключении к базе данных: {e}")





