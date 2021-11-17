""" Script for Symmetric Key Encryption/Decryption """
from cryptography.fernet import Fernet

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

    return dec_file

# sym_key_gen('p_symkey.key')
# sym_file_encrypt('symkey.key', 'login.csv')
# sym_file_decrypt('symkey.key', 'login.csv')