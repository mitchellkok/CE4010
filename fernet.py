""" Script for Symmetric Key Encryption/Decryption """
from cryptography.fernet import Fernet
import csv

def sym_key_gen(symkey_fn):
    key = Fernet.generate_key()    # generate new key
    
    # write key to .key file
    with open(symkey_fn, 'wb') as symkey_file:
        symkey_file.write(key)  


def sym_file_encrypt(symkey_fn, target_fn):
    # open key file
    with open(symkey_fn, 'rb') as symkey_file:    
        key = symkey_file.read()

    fernet = Fernet(key)    # initialise fernet object using key
    
    # open target file
    with open(target_fn, 'rb') as file:
        original = file.read()
        
    encrypted = fernet.encrypt(original)    # encrypt the data
    
    # write encrypted data to file
    with open(target_fn, 'wb') as enc_file:
        enc_file.write(encrypted)
        enc_file.close()
    return enc_file


def sym_file_decrypt(symkey_fn, target_fn):
    # open key file
    with open(symkey_fn, 'rb') as symkey_file:
        key = symkey_file.read()
    
    fernet = Fernet(key)    # initialise fernet object using key

    # open ciphertext file and read data
    with open(target_fn, 'rb') as enc_file:
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)    # decrypt the data
    
    # write decrypted data to file
    with open(target_fn, 'wb') as dec_file:
        dec_file.write(decrypted)
        dec_file.close()
    return dec_file
    

def fernet_read_file(symkey_fn, target_fn):
    # open key file
    with open(symkey_fn, 'rb') as symkey_file:
        key = symkey_file.read()
    fernet = Fernet(key)    # initialise fernet object using key

    # open ciphertext file and read data
    with open(target_fn, 'r') as file:
        encFile = bytes(file.read(), 'utf-8')

    decFile = fernet.decrypt(encFile).decode()  # decrypt data
    reader = csv.reader(decFile.splitlines())   # parse as csv
    return reader


def fernet_write_file(symkey_fn, target_fn, new_string):
    # open key file
    with open(symkey_fn, 'rb') as symkey_file:
        key = symkey_file.read()
    fernet = Fernet(key)    # initialise fernet object using key

    new_string = new_string.lstrip()    # remove leading newline
    encFile = fernet.encrypt(bytes(new_string, 'utf-8'))    # encrypt data

    # open ciphertext file and write data
    with open(target_fn, 'w') as file:
        file.write(encFile.decode("utf-8"))


def fernet_verify_file(symkey_fn, target_fn):
    # open key file
    with open(symkey_fn, 'rb') as symkey_file:
        key = symkey_file.read()
    fernet = Fernet(key)    # initialise fernet object using key

    # open ciphertext file and read data
    with open(target_fn, 'r') as file:
        encFile = bytes(file.read(), 'utf-8')

    fernet.extract_timestamp(encFile)   # verify data - throws error on failure
    print("File " + target_fn + " verified!")
    

# # sym_key_gen('files/p_symkey.key')
# sym_file_encrypt('files/u_symkey.key', 'files/users.csv')
# sym_file_encrypt('files/p_symkey.key', 'files/posts.csv')
# sym_file_decrypt('files/u_symkey.key', 'files/users.csv')
# sym_file_decrypt('files/p_symkey.key', 'files/posts.csv')
