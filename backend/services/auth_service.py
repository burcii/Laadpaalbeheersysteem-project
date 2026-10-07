from database import Database
import jwt
from datetime import datetime, timedelta, timezone
import re
from config import config
import pyotp
from werkzeug.security import generate_password_hash, check_password_hash

def validate_registration(data):
    email = data.get("email")
    password = data.get("password")
    email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    match True:
        case _ if not email or not password:
            return "Email en wachtwoord zijn vereist."
        case _ if not re.match(email_regex, email):
            return "Voer een geldig e-mailadres in."
        case _ if len(password) < 8:
            return "Minimaal 8 tekens vereist voor wachtwoord."
        case _ if not any(char.isdigit() for char in password):
            return "Minimaal één cijfer vereist in wachtwoord."
        case _:
            return None

def register_user(data):
    error = validate_registration(data)
    if error:
        return {"error": error}, 400
    
    # Two Factor authentication for admin registration.
    # /backend/config/config.py variable added called twofa.

    # TODO: For more information please read the documentation 
    # I wrote in the config.py.example for this token.
    # Be advised to read it carefully.

    # Default role
    role = "user"

    # Handle 2FA for admin/management roles
    twofa_code = data.get("twofa", "").strip()
    if twofa_code:
        # Check against management 2FA
        totp_mgmt = pyotp.TOTP(config.management_twofa)
        totp_admin = pyotp.TOTP(config.admin_twofa)
        if totp_mgmt.verify(twofa_code):
            role = "management"
        elif totp_admin.verify(twofa_code):
            role = "admin"
        else:
            return {"error": "Invalid 2FA code for elevated role"}, 401
    

    email = data["email"]
    password = data["password"]
    firstName = data.get("firstName", "")
    nameParticle = data.get("tussenvoegsel", "")
    lastName = data.get("lastName", "")
    adress = data.get("adress", "")
    zipcode = data.get("zipcode", "")
    country = data.get("country", "")
    phonenumber = data.get("phonenumber", 0)
    bankaccount = data.get("bankaccount", "")

    with Database() as db:
        db.execute_query("SELECT COUNT(*) as count FROM users WHERE email = %s", (email,))
        result = db.fetch_one()
        if result["count"]:
            return {"error": "Er bestaat al een account met dit e-mailadres."}, 409

        hashed_password = generate_password_hash(password)
        try:
            db.execute_query(
                """
                INSERT INTO users (email, password, adress, zipcode, country, firstName, nameParticle, lastName, phonenumber, bankaccount, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (email, hashed_password, adress, zipcode, country, firstName, nameParticle, lastName, phonenumber, bankaccount, role)
            )
            db.commit()
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            db.rollback()
            return {"error": str(e)}, 500

def login_user(email, password):
    if not email or not password:
        return {"error": "Email and password are required"}, 400

    with Database() as db:
        db.execute_query("SELECT * FROM users WHERE email = %s", (email,))
        user = db.fetch_one()

        if not user or not check_password_hash(user["password"], password, ):
            return {"error": "Ongeldige inloggegevens"}, 401

        payload = {
            "user_id": user["userID"],
            "exp": datetime.now(timezone.utc) + timedelta(hours=24 * 7)
        }
        token = jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")

        return {"token": token}, 200
