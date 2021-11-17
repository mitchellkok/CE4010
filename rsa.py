from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

def rsa_key_gen():
    keyPair = RSA.generate(1024)    # number of bits here
    pubKey = keyPair.publickey()
    print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
    pubKeyPEM = pubKey.exportKey()
    print(pubKeyPEM.decode('ascii'))
    print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
    privKeyPEM = keyPair.exportKey()
    print(privKeyPEM.decode('ascii'))

    keyData = {
        "publicKey" : pubKey,
        "keyPair" : keyPair
    }

    return keyData

def rsa_str_encrypt(pubKey, msg)  :
    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    print("Encrypted:", binascii.hexlify(encrypted))
    return encrypted    # return type bytes

def rsa_str_decrypt(keyPair, encrypted):
    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted    # return type bytes

# if __name__ == "__main__":
#     keyData = rsa_key_gen()
#     encrypted = rsa_str_encrypt(keyData["publicKey"], b'A message for encryption')
#     print(type(encrypted))

#     decrypted = rsa_str_decrypt(keyData["keyPair"], encrypted)
#     decrypted = decrypted.decode("utf-8") 
#     print('Decrypted:', decrypted, type(decrypted))
