"""
Serving the Landing Page
:author: Areeb Hussain
"""

from flask import Blueprint, render_template

bp = Blueprint('index', __name__)


# Serving the landing page
@bp.route("/")
@bp.route("/index")
def index():
    title = 'Home'
    return render_template('index.html', title=title)
