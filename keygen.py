from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

def main():
    from Crypto.PublicKey import RSA
    keyPair = RSA.generate(bits=1024)
    print(f"Public key:  (n={hex(keyPair.n)}, e={hex(keyPair.e)})")
    print(f"Private key: (n={hex(keyPair.n)}, d={hex(keyPair.d)})")
    with open('pub.key','w') as f:
        f.write(str(keyPair.e))
    with open('pvt.key','w') as f:
        f.write(str(keyPair.d))
    with open('key.n','w') as f:
        f.write(str(keyPair.n))
if __name__ == '__main__':
    main()
