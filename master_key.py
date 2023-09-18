from cryptography.fernet import Fernet
import os
import logging
import TwoFA as t

def get_master_key():
    with open("masterkey.key","rb") as f,open('masterkey.txt','rb') as g:
        key = Fernet(f.read())
        decrypted_message = key.decrypt(g.read()).decode()
        return decrypted_message
    

def key_gen():
    key = Fernet.generate_key()
    with open('masterkey.key', 'wb') as filekey:
        filekey.write(key)
    return key


def create_master_key():
    attempts = 3
    master_key = input('Enter Master key:')
    confirm = input('Confirm Master key:')
    choice = input('would you like to use 2 factor authentication (y/n):')
    if 'y' in choice.casefold():
        t.main()
        print('Sucessfully created!')
        

         
    while master_key!= confirm:
        if attempts == 0:
            return False
        master_key = input('Enter Master key:')
        confirm = input('Confirm Master key:')
        c-=1
    
    
    else:
        
        f = Fernet(key_gen())
        try:
            with open('masterkey.txt','wb') as g:
                encrypted_message = f.encrypt(master_key.encode())
                g.write(encrypted_message)
        
        except OSError as e:
            logging.error(f'{e}:Unable to save master key!')


def master_key_exists():
    if os.path.exists('masterkey.txt') and os.path.exists('masterkey.key') :
       return True
    

def update_masterkey():
    a = t.twofa_exists()
    if a:
        create_master_key()

    else:
        print('couldnt update masterkey!, No TWOFA found')


