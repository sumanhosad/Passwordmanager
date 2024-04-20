from cryptography.fernet import Fernet
import base64

def generate_key(hashed_master_password):
    """
    Generates a key from the hashed master password.
    """
    # Use the hashed master password directly as the key
    key = base64.urlsafe_b64encode(mp)
    return key

def encrypt_message(website_details, hashed_master_password):
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
