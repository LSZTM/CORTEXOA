import time
import qrcode
import smtplib as s
import smtplib as s,sys,re,random
import os


def twofa_exists():
    if os.path.exists('config.txt'):
        return True
    return False

def create_twofa(gmail):
    try:
        if gmail:
            with open('config.txt','w') as f:
                f.write(gmail)
        else:
            return 'Unable to setup'
    except OSError as e:
        return f'{e} ,occurred'



def check(gmail):
    attempts = 3
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while attempts>=0:
        if (re.search(regex, gmail)):
            print("Valid Email")
            return gmail
        else:
            gmail = input('Enter Gamil:')
            print("Invalid Email")
            check(gmail)
            attempts-=1
    else:
        print('Too many incorrect addresses!')


def get_data(gmail):
    sender_add = 'CORTEXOA@gmail.com'
    password = "rdhrxsyuvujnglta"
    receiver_add = check(gmail)
    subject = 'OTP for masterkey reset'
    otp = otp_gen()
    return sender_add,password,receiver_add,subject


def otp_gen():
    return random.randint(1000,9999)


def send_data(body):
    a,b,c,d = get_data(input('gmail:'))
    with s.SMTP('smtp.gmail.com',587) as f:
        f.starttls()
        try:
            f.login(a,b)
        except s.SMTPAuthenticationError as e:
            f.quit()
            print(f'{e} occurred')
            return False
        try:
            f.sendmail(from_addr = a,msg = 'Subject:{}\n\n{}'.format(d,body),to_addrs = c)
            print('Email Sent Sucessfully!')
            return c
        except:
            f.quit()
            print('Message Sending Failed')
            return False
    
def get_otp(_otp):
        try:
            otp = int(input('ENTER OTP:'))
            if otp == _otp:
                return True
            else:
                return False
        except ValueError:
            return False
            
def regenerate():
    _chc = input('regenerate OTP (y/n)?')
    if 'y' in _chc.casefold():
        _otp = otp_gen() 
        print('OTP regenerated!')
        s = 300
    
            


def intiate():
    _otp = otp_gen()
    gmail = send_data(_otp)
    if not gmail:
        return False
    os.system('cls')
    s = 300
    attempts = 5
    start = time.time()
    while s>=0 and attempts>=0:
        _verdict = False
        while True:
            if _verdict:
                return gmail
            temp = time.time()
            s = 300-(temp - start)
            if (start - temp)>5:
                os.system('cls')
                get_otp(_otp)
                if s<=270:
                    regenerate()
                    _verdict = get_otp(_otp)
                    
                    if not _verdict:
                        print('Incorrect OTP')
                        attempts-=1

                else:
                    print(f'Regenerate OTP (y/n) in {s-270}')
                    
                
            
            
    else:
        print('Too many incorrect attempts')
        return False


def main():
    gmail = intiate()
    if gmail:
        create_twofa(gmail)
        return True
    else:
        print('TWOFA failed')
        return False
    
main() 
        



    



