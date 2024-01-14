"""
Card Number Check Application
:author: Areeb Hussain
"""


from flask import Blueprint, render_template, request

bp = Blueprint('card_check', __name__)


def is_credit_card_valid(credit_card_number):
    # Remove spaces from the credit card number
    credit_card_number = ''.join(filter(str.isdigit, credit_card_number))

    # Apply the Luhn algorithm to validate the credit card number
    digits = list(map(int, credit_card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    total = sum(odd_digits)

    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))

    return total % 10 == 0


@bp.route("/card-check")
def card_check_page():
    title = 'Card Check'
    return render_template('card-check.html', title=title, message=None, is_valid=True)


@bp.route('/card-check', methods=['POST'])
def card_check_page_post():
    title = 'Card Check'
    credit_card_number = request.form.get('credit_card_number')
    is_valid = is_credit_card_valid(credit_card_number)

    message = f"The credit card number ({credit_card_number}) is " + ("valid!" if is_valid else "not valid!")

    # Process the credit card number here
    return render_template('card-check.html', title=title, message=message, is_valid=is_valid, credit_card_number=credit_card_number)