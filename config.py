import os

class Config(object):
    # Secret key used for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_key_if_not_set'

    # Integrate with a payment gateway: Stripe
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY') or 'your_stripe_public_key'
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'your_stripe_secret_key'

    # MongoDB configuration settings
    MONGODB_SETTINGS = {
        'db': 'a_records_store_db',  # Name of the MongoDB database
        'host': 'localhost',         # Host where MongoDB is running
        'port': 27017                # Port where MongoDB is running
    }

# Print the secret key for verification during development
print("SECRET_KEY:", Config.SECRET_KEY)
