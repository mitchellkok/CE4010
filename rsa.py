from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

def generateKey():
    keyPair = RSA.generate(3072)
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

def encryption(pubKey)  :
    msg = b'A message for encryption'
    encryptor = PKCS1_OAEP.new(pubKey)
    encrypted = encryptor.encrypt(msg)
    print("Encrypted:", binascii.hexlify(encrypted))
    return encrypted

def decryption(keyPair, encrypted):
    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted = decryptor.decrypt(encrypted)
    print('Decrypted:', decrypted)

if __name__ == "__main__":
    keyData = generateKey()
    encrypted = encryption(keyData["publicKey"])
    decryption(keyData["keyPair"], encrypted)
