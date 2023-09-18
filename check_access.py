from cryptography.fernet import Fernet
import master_key as m
import pickle
import db_control as d
encrypted = ''

def key_generator():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    return key


def encrypt():
    original = d.obtain_all()
    f = Fernet(key_generator())
    global encrypted 
    encrypted = f.encrypt(pickle.dumps(original))
    d.store_to_db(["NULL","NULL","NULL",str(encrypted)])
        

def decrypt():
    with open('filekey.key','rb') as f:
        fernet1 = Fernet(f.read())
    decrypted = fernet1.decrypt(encrypted)
    for i in pickle.loads(decrypted):
        d.store_to_db(i)


def check_access():
   if not m.master_key_exists():
        m.create_master_key()
        return True
   else:
        master_key = m.get_master_key()
        attempts = 3
        while attempts > 0:
            attempts -= 1
            user_input = input('Enter master key: ')
            if user_input != master_key:
                print('Wrong key, please try again.')
            else:
                return True
        return False




