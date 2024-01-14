"""
Brute Force Attack Application
:author: Areeb Hussain
"""

import os
from flask import Blueprint, render_template, request, current_app
import itertools
import time

# Setting up the Blueprint
bp = Blueprint('password_cracking', __name__)


# serving the initial page
@bp.route("/password-cracking", methods=['GET'])
def password_crack_page(title='Password Crack'):
    set2_message = "The password None does not exist in the dictionary!"  # to clear the messagebox on start
    return render_template('password-cracking.html', title=title, set1_message=None, set2_message=set2_message)


# Global variable to store the dictionary
dictionary = []


# Function to load the dictionary from the file
def load_dictionary():
    try:
        # Get the path to the static folder
        root = current_app.root_path

        # Construct the full file path
        file_path = os.path.join(root, 'resources', 'password_dictionary.txt')

        # Open the text file in read mode
        with open(file_path, 'r') as file:
            # Read each line of the file and add the word to the dictionary set
            for word in file:
                dictionary.append(word.strip())

    except FileNotFoundError:
        print(f"Error: The file 'password_dictionary.txt' not found.")
    except Exception as e:
        print(f"Error: {e}")


# Loading the dictionary when the app starts
@bp.before_request
def before_first_request():
    with current_app.app_context():
        load_dictionary()


# Function to iterate through combinations of passwords
def crack_password_set1(password_input):
    # Define the characters that can be used in the password
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
    tries = 0

    # Generating all possible combinations of 3 characters using itertools.product
    for password in itertools.product(characters, repeat=3):
        tries += 1

        # Converting the combination to a string and check if it matches the input password
        if ''.join(password) == password_input:
            # Return the cracked password, number of tries
            return ''.join(password), tries

    # If the password is not cracked, return None for the cracked password (or when performing set2 cracking function)
    return None, tries


# Function to check if the password matches any word in the dictionary
def crack_password_set2(password_input):
    # Start the timer
    start_time = time.time()

    tries = 0

    # Check if the input password matches any word in the dictionary
    for word in dictionary:
        tries += 1
        if password_input == word:
            # Stop the timer
            end_time = time.time()
            # Calculate the time taken in seconds
            time_taken = (end_time - start_time) * 1000
            # Return the cracked password, number of tries, and time taken
            return word, tries, time_taken

    # If the password is not found in the dictionary, return None for the cracked password
    return None, tries, None


# main post function
@bp.route('/password-cracking', methods=['POST'])
def password_crack_post(title='Password Crack'):
    # getting inputs from form
    set1_password_input = request.form.get('set1_password')
    set2_password_input = request.form.get('set2_password')

    # Calling the crack_password function to attempt to crack the password
    # for set1
    set1_start_time = time.time()
    set1_cracked_password, set1_tries = crack_password_set1(set1_password_input)
    set1_end_time = time.time()
    set1_time_taken = (set1_end_time - set1_start_time) * 1000  # Time in milliseconds

    # for set2
    set2_start_time = time.time()
    set2_cracked_password, set2_tries, set2_time_taken = crack_password_set2(set2_password_input)
    set2_end_time = time.time()
    set2_time_taken = (set2_end_time - set2_start_time) * 1000  # Time in milliseconds

    set1_message = f"Your password is '{set1_cracked_password}', and it was cracked in {set1_tries} tries ({set1_time_taken:.4f} milliseconds)!" if set1_cracked_password else None
    set2_message = f"Your password is '{set2_cracked_password}', and it was cracked in {set2_tries} tries ({set2_time_taken:.4f} milliseconds)!" if set2_cracked_password \
        else f"The password {'*' * len(set2_password_input) if set2_password_input else None} does not exist in the dictionary!"
    set2_message_style = 'msg-green' if set2_cracked_password else 'msg-red'

    return render_template('password-cracking.html', title=title, set1_message=set1_message, set2_message=set2_message,
                           set2_message_style=set2_message_style, set1_password=set1_password_input,
                           set2_password=set2_password_input)
