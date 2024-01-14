"""
Encryption end of Message Encryption-Decryption Application
:author: Areeb Hussain
"""

from flask import Blueprint, render_template, request, redirect, url_for, session
import random
import hashlib

# Blueprint setup
bp = Blueprint('text_encryption', __name__)
app_dir = 'text-encryption-app/'


# Generate random key of a given length
def generate_key(length):
    # Generate random bytes
    key = [random.randint(0, 255) for _ in range(length)]
    return bytes(key)


# XOR cipher for encryption
def xor_cipher(data, key):
    cipher = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        # XOR each byte with key
        cipher.append(byte ^ key[i % key_len])
    return bytes(cipher)


# Convert string to bytes
def str_to_bytes(string):
    return bytes(string, 'utf-8')


# Main function for encryption
def encrypt(message2, key):
    msg_bytes = str_to_bytes(message2)
    encrypted_msg = xor_cipher(msg_bytes, key)
    return encrypted_msg


# Route for GET request
@bp.route("/text-encrypt", methods=['GET'])
def text_encryption_app(title='Text Encryption App'):
    # Show the HTML form
    return render_template(app_dir + 'message-encryption.html', title=title)


# Route for POST request
@bp.route("/text-encrypt", methods=['POST'])
async def text_encryption_app_post(title='Text Encryption App'):
    # Get messages from form
    message1 = request.form.get('message1')
    message2 = request.form.get('message2')

    # Generate a 16-byte key
    shared_key = generate_key(16)

    # Save key in session
    session['key'] = shared_key.hex()

    # Encrypt message1
    cipher = encrypt(message1, shared_key)
    cipher_hex = cipher.hex()

    # Combine messages and create hash
    combined_msg = f"{cipher_hex}||{message2}"
    hash1 = hashlib.sha1(combined_msg.encode()).hexdigest()

    # Redirect to decryption page
    return redirect(url_for('text_decryption.text_decryption_page', title=title, message=combined_msg, hash=hash1))
