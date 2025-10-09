import pymysql

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        database="plant_pulse_db",
        password="P@$$w0rd",
        cursorclass=pymysql.cursors.DictCursor
    )