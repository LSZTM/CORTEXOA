import random
import json as j
from cryptography.fernet import Fernet
import re
import os
import shutil
import csv
import sys
import string
import mysql.connector as mys
obj = mys.connect(host = 'localhost',user='root',password = 'root',database = 'password_manager')
cursor = obj.cursor()

def currentfile_location_writer(a = os.path.join(f'{os.getcwd()}', "passwords.txt")):
    if not os.path.exists(a):
        with open(a, "w"):
            pass
    with open('text_file.txt', 'w') as f:
        f.write(a)
    return a

def currentfile_location():
    if os.path.exists(os.path.join(f'{os.getcwd()}','text_file.txt')):
            with open('text_file.txt') as f:
                a = f.read()
                if os.path.exists(a):
                    return a
                else:
                    currentfile_location_writer()
    else:
        currentfile_location_writer()

def csv_filelocation_writer(a=os.path.join(f'{os.getcwd()}', "passwords.csv")):
    if not os.path.exists(a):
        with open(a, "w"):
            pass
    with open("text_file.csv", "w") as f:
        f.write(a)
    return a

def csv_filelocation():
    if os.path.exists(os.path.join(f'{os.getcwd()}','text_file.csv')):
        with open('text_file.csv') as f:
            a = f.read()
            if os.path.exists(a):
                return a
            else:
                csv_filelocation_writer()
    else:
        csv_filelocation_writer()


def key_generator():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)
    return key


def encrypt():
    currentfileloc = currentfile_location()
    csvfileloc = csv_filelocation()
    with open(currentfileloc,"rb") as filekey:
        original = filekey.read()
    fernet1 = Fernet(key_generator())
    encrypted = fernet1.encrypt(original)
    with open(currentfileloc,"wb") as f:
        f.write(encrypted)
    with open(csvfileloc,"rb") as filekey:
        original1 = filekey.read()
    encrypted = fernet1.encrypt(original)
    with open(csvfileloc, 'wb') as f:
        f.write(encrypted)
    dest_path = f'{currentfileloc}'+'.enc'
    dest_path1 = f'{csvfileloc}'+'.enc'
    enc_file_name(currentfileloc, dest_path)
    enc_file_name(csvfileloc, dest_path1)
    currentfile_location_writer(dest_path)
    csv_filelocation_writer(dest_path1)

def enc_file_name(a,b):
    os.rename(a,b)




def decrypt():
    currentfileloc = currentfile_location()
    csvfileloc = csv_filelocation()
    dest_path = f'{currentfileloc}'.replace('.enc','')
    dest_path1 = f'{csvfileloc}'.replace('.enc','')
    print(dest_path,dest_path1)
    enc_file_name(currentfileloc,dest_path)
    enc_file_name(csvfileloc,dest_path1)
    currentfile_location_writer(dest_path)
    csv_filelocation_writer(dest_path1)

    with open('filekey.key','rb') as f:
        fernet1 = Fernet(f.read())
    with open(dest_path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet1.decrypt(encrypted)
    with open(dest_path, "w") as f:
        f.write(decrypted.decode())

    # opening the file in write mode and
    # writing the decrypted data
    with open(dest_path1,"rb") as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet1.decrypt(encrypted)
    with open(dest_path1, "w") as f:
        f.write(decrypted.decode())








def check_access():
    csv_filelocation()
    currentfile_location()
    if not master_key_exists():
        create_master_key()
        return True

    else:
        master_key = get_master_key()
        attempts = 3
        while attempts > 0:
            attempts -= 1
            user_input = input('Enter master key: ')
            if user_input != master_key:
                print('Wrong key, please try again.')
            else:
                return True
    


    return False


def get_master_key():
    with open("masterfile.txt") as f:
        a = f.read()
        return a



def create_master_key():
    with open("masterfile.txt", 'w') as f:
        mk = input("Set Master Key:")
        mk1 = input("Confirm Master Key:")
        while mk1!= mk:input("Confirm Master Key:")
        f.write(mk)
        print("master key successfully created")



def master_key_exists():
    if os.path.exists((os.path.join(f"{os.getcwd()}", "masterfile.txt"))) :
        with open((os.path.join(f"{os.getcwd()}", "masterfile.txt"))) as f:
            if len(f.read())!=0:
                return True
    else:
        return False


def final_password():
    set = string.ascii_letters + string.digits + string.punctuation
    try:
        length = int(input("enter  desired length of password:"))
    except TypeError:
        print("TypeError: enter a number")
    password = ''.join([random.SystemRandom().choice(set) for _ in range(length)])
    return password


def exist_check(a, b):
    currentfileloc = currentfile_location()
    with open (currentfileloc) as f:
        new = f.read().split('\n')
        print(new)
        if len(new)>1:
            a1 = [j.loads(i) for i in new if i !='']
            print(a1)
            for i in a1:
                if a in i.keys() and b in i[a]:
                    return True
        else:
            return False





def view_func():
    c = currentfile_location()
    with open(c) as f:
        return f.read()



def edit(a,b):
    currentfileloc,csvv = currentfile_location(),csv_filelocation()
    try:
        with open(currentfileloc) as f:
            a1 = j.loads(f.read())

    except:
        print("no saves found!")
        return None

    if a not in a1.keys(): return "does not exist"
    elif b not in [i[0] for i in a1.values()]:return "does not exist"
    for i in a1.keys():
        if a1[i][0] == b:
            option = input("1.regenarate password,\n2.manually change password,\n3.delete save\n:")
            if option not in ("1","2","3"):return False
            elif option == "1":
                password = final_password()
                a1[i][1] == password
                cursor.execute("update pwm set password =(%s) where Domain = (%s) and Gmail = (%s)",(a,b,a1[i][1]))
                print(a1[i])
                return "successful"
            elif option == "2": a1[i][1] = input("enter password:")
            elif option == "3": del a1[i][1]
            write_func(b)
            csv_operations(b)



def write_func(l):
    currentfileloc = currentfile_location()
    with open(currentfileloc, "a") as a:
        a.write(j.dumps(l)+'\n')




def copyanother_csvfile_remove_exsisting_file():
    currentfile = csv_filelocation()
    newfile = input("enter file path")
    while not os.path.exists(newfile) and ".csv" not in newfile:newfile = input("enter file path, should be csv:")
    shutil.copyfile(currentfile,newfile)
    os.remove(currentfile)
    csv_filelocation_writer(newfile)


def copytoanother_file_remove_exisitingfile():
    currentfileloc = currentfile_location()
    newfile = input("enter file path:")
    while not os.path.exists(newfile) or not ".txt" not in newfile:newfile = input("enter file path:")
    shutil.copyfile(currentfileloc, newfile)
    os.remove(currentfileloc)
    currentfile_location_writer(currentfileloc)
def csv_operations(l):
    csvfileloc = csv_filelocation()
    with open(csvfileloc, 'a+', newline="") as csvfile:
        f = csv.writer(csvfile, delimiter=' ')
        f.writerow(j.dumps(l))



def phone_number(s):
    regex = re.compile(r"^(?:\+44|0)7\d{9}$")
    return regex.match(s)

   


def check(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    if (re.search(regex, email)):
        print("Valid Email")
        return (email)
    else:
        print("Invalid Email")
        check(input("enter email:"))


def del_func():
    currentfileloc = currentfile_location()
    csvfileloc = csv_filelocation()
    if os.path.exists(currentfileloc):
        os.remove(currentfileloc)
        print("sucessful")
        exit()
    else:
        print("file does not exist")
        exit()




def password_generator():
    domainname = str(input("enter domain name :"))
    username = str(input("enter username :"))


def instagram():
    email = input("enter email: ")
    b = check(email)
    a = exist_check("instagram",b)
    if not a:
        password = final_password()
        L = {'instagram': [email, password]}
        cursor.execute('insert into pwm values(("instagram"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)
    else:print("account aldready exists")



# write_func(password)
def facebook():
    email = input("enter email: ")
    b = check(email)
    a = exist_check("facebook", b)
    if not a:
        password = final_password()
        L = {'facebook': [f'{email}', f"{password}"]}
        cursor.execute('insert into pwm values(("facebook"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)

    else:
        print("account aldready exists")


def twitter():
    email = input("enter email: ")
    b = check(email)
    a = exist_check("twitter", b)
    if not a:
        password = final_password()
        L = {'twitter': [f'{email}', f"{password}"]}
        cursor.execute('insert into pwm values(("twiiter"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)
    else:
        print("account aldready exists")




def netflix():
    email = input("enter email: ")
    b = check(email)
    a = exist_check("netflix", b)
    if not a:
        password = final_password()
        L = {'netflix': [f'{email}', f"{password}"]}
        cursor.execute('insert into pwm values(("netflix"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)
    else:
        print("account aldready exists")




def amazon():
    email = input("enter emaiil: ")
    b = check(email)
    a = exist_check("amazon", b)
    if not a:
        password = final_password()
        L = {'amazon': [f'{email}', f"{password}"]}
        cursor.execute('insert into pwm values(("amazon"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)
    else:
        print("account aldready exists")




def gmail():
    email = input("enter email: ")
    b = check(email)
    a = exist_check("gmail", b)
    if not a:
        password = final_password()
        b = passcheck(password)
        while b == False:
            password = final_password()
            b = passcheck(password)
        m = password
        L = {'gmail': [f'{email}', f"{password}"]}
        cursor.execute('insert into pwm values(("gmail"),(%s),(%s));', (email, password))
        write_func(L)
        csv_operations(L)
    else:
        print("account aldready exists")




def reddit():
    email = input("enter email: ")
    check(email)
    a = final_password()
    b = passcheck(a)
    if not a:
        while b == False:
            a = final_password()
            b = passcheck(a)
        reddit_pass = a
        L = {'gmail': [f'{email}', f"{reddit_pass}"]}
        cursor.execute('insert into pwm values(("reddit"),(%s),(%s));', (email, reddit_pass))
        write_func(L)
        csv_operations(L)
    else:
        print("account aldready exists")


def passcheck(a):
    y = []
    for x in a:
        y.append(x)
    i = 0
    newvar = True
    while i < len(y):
        if [y[i]] != [y[i + 1]] and y[i]+y[i+1]!="\n":
            i = i + 2
            newvar = True
        else:
            newvar = False
            break
        return newvar


def new_accnt_details():
    email = input("enter email")
    check(email)
    domain = input("enter domain:")
    if domain.lower() in ['instagram', 'facebook', 'twitter', 'netflix', 'gmail', 'reddit', 'amazon']:
        print("that domain is availabe in our prebuilts, please select the appropriate option")
        main_menu()
    password = final_password()
    L = {f'{domain}': [f'{email}', f"{password}"]}
    cursor.execute('insert into pwm values((%s),(%s),(%s));', (domain,email, password))
    write_func(L)
    csv_operations(L)



def emailgen():
    num_of_chars = int(input("enter number of characters between 4 to 20: "))
    if num_of_chars < 4 or num_of_chars > 20:
        print("number of chars excceding limit")
        emailgen()

    else:
        listofletters = [string.digits, string.ascii_lowercase, string.ascii_uppercase]
        letters = "".join(listofletters)
        emailformat =  "@gmail.com"
        emailgenerated = "".join(random.choices(letters, k = num_of_chars))+emailformat
        print(emailgenerated)


def main_menu():
    print("⁺˚*•̩̩͙✩•̩̩͙*˚⁺‧͙⁺˚*•̩̩͙⋆⁺₊⋆Ƹ̵̡Ӝ̵̨̄Ʒ⋆⁺₊⋆•̩̩͙*˚⁺‧͙⁺˚*•̩̩͙✩•̩̩͙*˚⁺‧͙")
    print("1.generate a password")
    print("2.managing password saves")
    print("3.file settings")
    print("4.add an existing account for saving")
    print("5.generate new gmail id")
    print("6.exit program")
    print("⁺˚*•̩̩͙✩•̩̩͙*˚⁺‧͙⁺˚*•̩̩͙⋆⁺₊⋆Ƹ̵̡Ӝ̵̨̄Ʒ⋆⁺₊⋆•̩̩͙*˚⁺‧͙⁺˚*•̩̩͙✩•̩̩͙*˚⁺‧")
    action = input("enter key :")
    if (action == '1'):

        print(
            "╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱"
            "\nWhich of the following sites would you like to generate a password for:\n1.instagram\n2.facebook\n3.twitter\n4.netflix\n5.reddit\n6.amazon\n7.gmail\n8.other\n9.menu"
            "\n╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱╲⎝⧹╲⎝⧹⧸⎠╱⧸⎠╱")
        key = input("enter key :")

        if (key == '1'):
            instagram()
        elif (key == '2'):
            facebook()
        elif (key == '3'):
            twitter()
        elif (key == '4'):
            netflix()
        elif (key == '5'):
            reddit()
        elif (key == '6'):
            amazon()
        elif (key == '7'):
            gmail()
        elif (key == "8"):
            new_accnt_details()
        else:
            print("key does not match!\n enter a valid option")
            main_menu()
    elif (action == '2'):
        print("1.view saved passwords"
              "\n2.edit saved passwords")
        keyforaction_2 = input("enter key:")

        if (keyforaction_2 == "1"):
            print(view_func())
        elif (keyforaction_2 == "2"):

            edit(input("domain:"),input("mail:"))
        else:
            print("thats not a valid key!")
            encrypt()
            exit()
    elif (action == '3'):
        key = input("\nchoose the following actions:\n1.delete file\n2.copy data to another file and delete existing file\n:")
        if key not in ['1', '2']:
            print("\nplease choose a valid key")
            main_menu()
        elif (key == "1"):
            del_func()
        elif (key == '2'):
            print("\nAre you sure want to permanently delete this file and move dta to a new file")
            key = input("1.yes""\n2.no")
            if key == '1':
                copytoanother_file_remove_exisitingfile()
            else:
                obj.commit()
                encrypt()
                exit()





    elif (action == '4'):
        new_accnt_details()

    elif (action == '5'):
        emailgen()


    elif (action == '6'):
        print("exiting")
        print(
            "💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟💠⃟")
        encrypt()
        obj.commit()
        sys.exit()


if ".enc" not in f'{currentfile_location()}'and ".enc" not in f'{csv_filelocation()}' and not os.path.exists(os.path.join(f'{os.getcwd()}','filekey.key')):
    pass
else:
    decrypt()
if check_access():
    a = 'y'
    try:
        while a.lower() == 'y':

            print("Welcome to password Generator and Manager!")
            print("press the key to perform the required action!")
            main_menu()
            a = input("would you like to continue?(y/n) :")
            if a.lower() == '':
                obj.commit()
                encrypt()
                print("no input detected")
                sys.exit()
        else:
            obj.commit()
            encrypt()
            sys.exit()
    except KeyboardInterrupt:
        encrypt()
        obj.commit()
        print(" program interrupted")
        sys.exit(0)
        
else:
    sys.exit()












