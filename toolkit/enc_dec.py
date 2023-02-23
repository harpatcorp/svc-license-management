import os

from cryptography.fernet import Fernet


class EncDec:

    def __init__(self):
        self._key = os.environ["enc_key"]

    def encrypt_file(self, original_file, encrypted_file):
        f = Fernet(self._key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open(encrypted_file, 'wb') as file:
            file.write(encrypted)

    def decrypt_file_data(self, encrypted_file_data):
        f = Fernet(self._key)

        decrypted_data = f.decrypt(encrypted_file_data)

        return decrypted_data
