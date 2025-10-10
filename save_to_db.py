from db import get_connection
from arduino import arduino
import json

connection = get_connection()
cursor = connection.cursor()

def save_pin(pin):
    try:
        sql = "INSERT INTO dummy_table(pin_number) VALUES(%s)"
        cursor.execute(sql, (pin, ))
        connection.commit()
        return {"status" : True}
    except Exception as e:
        print(f"Error : {e}")
        return {"status" : False}
    
def get_reserved_pins():
    try:
        sql = "SELECT pin_number FROM dummy_table"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error : {e}")
        return {"status" : False}