import mysql.connector as mys
import password_generator as p
import _log as c
import logging


obj = mys.connect(host = 'localhost',user='root',password = 'root',database = 'password_manager')
cursor = obj.cursor()
logger = c.create_logger()
logging.basicConfig(filename= logger, level=logging.INFO)


    
    

def obtain_all():
    try:

        cursor.execute('select * from pwm; ')
        return cursor.fetchall()
    
    except:
        logging.error('Unable to obtain info from db')


def store_to_db(_data):
    try:
        if not exists_check(_data):
            
            cursor.execute('insert into pwm values(%s,%s,%s,%s);',(_data[0],_data[1],_data[2],_data[3]))
            obj.commit()
            print('Saved Successfully')
        else:
            print('Data Aldready exists')
    except:
        logging.error('error while writing to database')
        

def remove_from_db(_data):
    try:
        if  exists_check(_data):
            cursor.execute('delete from pwm where domain = %s and gmail = %s and password = %s;',(_data[0],_data[1],_data[2],))
            print('removed Successfully')
        else:
            print('No such data exists!')
        obj.commit()
        
    except:
        logging.error('error while removing from database')

def exists_check(_data):
    
    try:
        cursor.execute('select * from pwm where domain = %s and gmail = %s and password = %s;',(_data[0],_data[1],_data[2],))
        if cursor.fetchone():
            return True
        return False
    
    except:
        logging.error('error while checking database')


