"""
Flask Application Setup
:author: Areeb Hussain
"""

# Import Flask framework and custom route handlers from 'routes' module
from flask import Flask
from routes import index, card_check, hamming_code, password_crack, message_encryption, message_decryption


def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Register blueprints for different routes
    app.register_blueprint(index.bp)
    app.register_blueprint(card_check.bp)
    app.register_blueprint(hamming_code.bp)
    app.register_blueprint(password_crack.bp)
    app.register_blueprint(message_encryption.bp)
    app.register_blueprint(message_decryption.bp)

    app.secret_key = 'jkbhdsf89y89234h5f'

    # filter to provide enumerate functionality
    @app.template_filter('enumerate')
    def enumerate_func(iterable, start=0):
        return enumerate(iterable, start=start)

    # Return the configured Flask app
    return app


if __name__ == '__main__':
    # Create and run the Flask app in debug mode
    app = create_app()
    app.run(debug=True)
