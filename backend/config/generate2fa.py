import pyotp

# Generate a new secret
totp_secret = pyotp.random_base32()
print(totp_secret)  # Save this in the user's row in the database