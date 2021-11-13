from cryptography.fernet import Fernet

key = Fernet.generate_key() #variable to generate the key
file = open ("encryption_key.txt", "wb") # open the file
file.write(key) # write the key to the file
file.close()
