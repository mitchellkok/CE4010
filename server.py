import pandas as pd

from fernet import *
from rsa import *

def open_csv(login_csv_fn, symkey_fn):
    sym_file_decrypt(symkey_fn, login_csv_fn)
    df = pd.read_csv(login_csv_fn)
    sym_file_encrypt(symkey_fn, login_csv_fn)

    return df


def verify_login(incoming, rsa_key_data, login_df):
    print(login_df)
    # decrypted_incoming = rsa_str_decrypt(rsa_key_data["keyPair"], incoming)


if __name__ == "__main__":
######## SETUP ########
    # key_data = rsa_key_gen() # generate public/encryption keypair for RSA
    
    l_csv_fn = 'login.csv'
    l_sym_key_fn = 'l_symkey.key'

    p_csv_fn = 'posts.csv'
    p_sym_key_fn = 'p_symkey.key'
    # sym_key_gen(sym_key_fn)   # uncomment if need to regenerate key

    # open files
    l_df = open_csv(l_csv_fn, l_sym_key_fn)
    p_df = open_csv()
    verify_login("","", l_df)


######## MAIN LOOP ########
