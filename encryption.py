from cryptography.fernet import Fernet
from dotenv import load_dotenv
import argparse
import os


def encryptFile(filename):

    load_dotenv()

    fernet = Fernet(os.getenv('FERNET_ENCRYPTION_KEY'))

    with open(filename,'rb') as file_to_encrypt:
        
        plain_data = file_to_encrypt.read()
        encrypted_data = fernet.encrypt(plain_data)

    with open(filename,'wb') as file_to_encrypt:
        file_to_encrypt.write(encrypted_data)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Encrypt a file with Fernet")
    parser.add_argument('filename', help='Path to the decrypted file')
    args = parser.parse_args()

    try:
        encryptFile(args.filename)
    except Exception as e:
        print(f"Encryption failed: {e}")



