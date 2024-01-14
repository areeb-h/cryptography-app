"""
Hamming Code Correction Application
:author: Areeb Hussain
"""

from flask import Blueprint, render_template, request

bp = Blueprint('hamming_code', __name__)


def error_check(binary, parity):
    parity = 1 if parity == "odd" else 0

    bits = [int(bit) for bit in binary]

    p4_check = 0 if sum(bits[i] for i in [0, 1, 2, 3]) % 2 == int(parity) else 4
    p2_check = 0 if sum(bits[i] for i in [0, 1, 4, 5]) % 2 == int(parity) else 2
    p1_check = 0 if sum(bits[i] for i in [0, 2, 4, 6]) % 2 == int(parity) else 1

    dec = (p4_check + p2_check + p1_check) - 1
    pos = ["p1", "p2", "d3", "p4", "d5", "d6", "d7"]

    # to flip the position
    index = [6, 5, 4, 3, 2, 1, 0]

    error_row = [str(bits[index[dec]]) if i == index[dec] else bit for i, bit in enumerate(bits)]
    error_row = ["Error is at " + pos[dec]] + error_row

    corrected_row = [str(bits[index[dec]]) if i == index[dec] else bit for i, bit in enumerate(bits)]
    corrected_row[index[dec]] = 1 if bits[index[dec]] == 0 else 0
    corrected_row = ["Error corrected"] + corrected_row

    return error_row, corrected_row, dec


@bp.route("/hamming-code")
def hamming_code_page(title='Hamming Code Correction'):
    return render_template('hamming-code.html', title=title, message=None)


@bp.route('/hamming-code', methods=['POST'])
def hamming_code_post(title='Hamming Code Correction'):
    hamming_code = request.form.get("hamming_code")
    parity_bit = request.form.get("parity_bit")

    binary = [int(bit) for bit in hamming_code]
    # Check if the input binary string is of length 7
    if len(binary) != 7:
        raise ValueError("Please enter a 7-bit Hamming code.")

    # Hamming code error checking and correction logic
    header = [f"{parity_bit} parity check", "d7", "d6", "d5", "p4", "d3", "p2", "p1"]
    error_row, corrected_row, dec = error_check(binary, parity_bit)

    position = 7 - dec

    if position > 7 or position < 1:  # Check if the error_row list is empty
        message = "No error found in the hamming code"
    else:
        message = None

    print(f"message = {message if message is not None else ''}")

    return render_template("hamming-code.html", parity_bit=parity_bit, hamming_code=hamming_code, title=title,
                           header=header, error_row=error_row, corrected_row=corrected_row,
                           message=message, position=position)
