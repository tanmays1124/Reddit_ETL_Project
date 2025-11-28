from cryptography.fernet import Fernet
from dotenv import load_dotenv
import argparse
import os


def decryptFile(filename):

    load_dotenv()

    fernet = Fernet(os.getenv('FERNET_ENCRYPTION_KEY'))

    with open(filename,'rb') as file_to_decrypt:
        
        encrypted_data = file_to_decrypt.read()
        decrypted_data = fernet.decrypt(encrypted_data)

    with open(filename,'wb') as file_to_decrypt:
        file_to_decrypt.write(decrypted_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Decrypt a file encrypted with Fernet")
    parser.add_argument('filename', help='Path to the encrypted file')
    args = parser.parse_args()

    try:
        decryptFile(args.filename)
    except Exception as e:
        print(f"Decryption failed: {e}")

