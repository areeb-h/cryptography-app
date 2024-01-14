"""
Decryption end of Message Encryption-Decryption Application
:author: Areeb Hussain
"""

import hashlib
from flask import Blueprint, render_template, request, session

# Setting up the Blueprint
bp = Blueprint('text_decryption', __name__)


# XOR cipher (can be used for both encryption and decryption)
def xor_cipher(data, key):
    result = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_len])
    return result


# Decipher function that uses the xor_cipher and decodes to utf-8
def xor_decipher(ciphertext, key):
    decrypted = xor_cipher(ciphertext, key)
    return decrypted.decode('utf-8')


# Route for GET request
@bp.route("/text-decrypt", methods=['GET'])
def text_decryption_page(title='Text Encryption App'):
    # Retrieve encrypted message and hash from URL
    combined_message = request.args.get('message')
    sha1_hash = request.args.get('hash')

    # Splitting combined message
    parts = combined_message.split('||')
    ciphertext = parts[0]
    message1 = parts[1]

    # Calculate hash and compare
    calc_hash = hashlib.sha1(combined_message.encode()).hexdigest()
    if calc_hash != sha1_hash:
        print("Hash verification failed")
        return "Hash mismatch!"

    return render_template('text-encryption-app/message-decryption.html', title=title, ciphertext=ciphertext,
                           message1=message1, decrypted=None)


# Route for POST request
@bp.route("/text-decrypt", methods=['POST'])
def text_decryption_post(title='Text Encryption App'):
    # Retrieve the key stored in session
    key_hex = session.get('key')
    if key_hex is None:
        return "No key in session. Go back and encrypt first."

    # Retrieve ciphertext and message1 from form
    ciphertext_hex = request.form.get('ciphertext')
    message1 = request.form.get('message1')

    # Convert hex to bytes
    key = bytes.fromhex(key_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)

    # Decrypt and display
    decrypted_message = xor_decipher(ciphertext, key)

    return render_template('text-encryption-app/message-decryption.html', title=title, ciphertext=ciphertext_hex,
                           message1=message1, decrypted=decrypted_message)
