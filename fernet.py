""" Script for Symmetric Key Encryption/Decryption """
from cryptography.fernet import Fernet
import csv

def sym_key_gen(symkey_fn):
    key = Fernet.generate_key()    # key generation
    
    # string the key in a file
    with open(symkey_fn, 'wb') as symkey_file:
        symkey_file.write(key)  


def sym_file_encrypt(symkey_fn, target_fn):
    with open(symkey_fn, 'rb') as symkey_file:    # opening the key
        key = symkey_file.read()
    
    fernet = Fernet(key)    # using the generated key
    with open(target_fn, 'rb') as file:    # opening the original file to encrypt
        original = file.read()
        
    encrypted = fernet.encrypt(original)    # encrypting the file
    
    # opening the file in write mode and writing the encrypted data
    with open(target_fn, 'wb') as enc_file:
        enc_file.write(encrypted)
        enc_file.close()
    
    print("\tENCRYPTED:", target_fn, "using", symkey_fn)
    return enc_file


def sym_file_decrypt(symkey_fn, target_fn):
    with open(symkey_fn, 'rb') as symkey_file:    # opening the key
        key = symkey_file.read()

    fernet = Fernet(key)    # using the key
    with open(target_fn, 'rb') as enc_file:    # opening the encrypted file
        encrypted = enc_file.read()
    
    decrypted = fernet.decrypt(encrypted)    # decrypting the file
    
    # opening the file in write mode and writing the decrypted data
    with open(target_fn, 'wb') as dec_file:
        dec_file.write(decrypted)
        enc_file.close()

    print("\tDECRYPTED: ", target_fn, "using", symkey_fn)
    return dec_file

def fernet_read_file(symkey_fn, target_fn):
    with open(symkey_fn, 'rb') as symkey_file:    # opening the key
        key = symkey_file.read()
    fernet = Fernet(key)    # using the key

    with open(target_fn, 'r') as file:
        encFile = bytes(file.read(), 'utf-8')

    decFile = fernet.decrypt(encFile).decode()
    reader = csv.reader(decFile.splitlines())
    return reader


def fernet_write_file(symkey_fn, target_fn, new_string):
    with open(symkey_fn, 'rb') as symkey_file:    # opening the key
        key = symkey_file.read()
    fernet = Fernet(key)    # using the key

    new_string = new_string.lstrip()    # remove leading newline
    encFile = fernet.encrypt(bytes(new_string, 'utf-8'))

    with open(target_fn, 'w') as file:
        file.write(encFile.decode("utf-8"))

def fernet_verify_file(symkey_fn, target_fn):
    with open(symkey_fn, 'rb') as symkey_file:    # opening the key
        key = symkey_file.read()
    fernet = Fernet(key)    # using the key

    with open(target_fn, 'r') as file:
        encFile = bytes(file.read(), 'utf-8')

    fernet.extract_timestamp(encFile)
    print("File " + target_fn + " verified!")
    

# # sym_key_gen('p_symkey.key')
# sym_file_encrypt('u_symkey.key', 'users.csv')
# sym_file_encrypt('p_symkey.key', 'posts.csv')
# sym_file_decrypt('u_symkey.key', 'users.csv')
# sym_file_decrypt('p_symkey.key', 'posts.csv')
 
# csv = fernet_read_file('u_symkey.key', 'users.csv')
# print(csv)
# print(type(csv))