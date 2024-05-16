from cryptography.fernet import Fernet
import base64
import random
import string


from cryptography.fernet import Fernet

def generate_key(hashed_mp):
    """
    Generate a 32-byte key from the hashed master password.
    """
    # Convert the hexadecimal string to bytes
    hashed_bytes = bytes.fromhex(hashed_mp)
    
    # Base64 encode the bytes to get a valid Fernet key
    key = base64.urlsafe_b64encode(hashed_bytes)
    
    return key


def encrypt_message(website_details, mp):
    """
    Encrypts website details using the hashed master password.
    """
    key = generate_key(mp)
    cipher_suite = Fernet(key)

    # Convert website details to string
    plaintext = ',,'.join(website_details)
    
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
    website_details = decrypted_message.split(',,')
    return website_details

