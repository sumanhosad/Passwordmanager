from cryptography.fernet import Fernet
import base64
import random
import string


from cryptography.fernet import Fernet

def generate_key(mp):
    """
    Generates a key from the hashed master password.
    """
    return mp.encode()

def encrypt_message(website_details, mp):
    """
    Encrypts website details using the hashed master password.
    """
    key = generate_key(mp)
    cipher_suite = Fernet(key)

    # Convert website details to string
    plaintext = ','.join(website_details)
    
    # Encrypt the plaintext
    encrypted_message = cipher_suite.encrypt(plaintext.encode())
    return encrypted_message

def decrypt_message(encrypted_message, mp):
    """
    Decrypts an encrypted message using the hashed master password.
    """
    key = generate_key(mp)
    cipher_suite = Fernet(key)

    # Decrypt the message
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()

    # Split decrypted message into website details
    website_details = decrypted_message.split(',')
    return website_details

