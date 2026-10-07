import os
import re
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database


def verify_password(password, hashed_password):
    try:
        return check_password_hash(hashed_password, password)

    except Exception as e:
        print(f"Fout bij het verifiëren van het wachtwoord: {e}")
        return False


def validate_password(password):
    """
    - Password must be at least 8 characters long
    - Password must contain at least one uppercase letter
    - Password must contain at least one number
    """
    errors = []
    if len(password) < 8:
        errors.append("Wachtwoord moet minimaal 8 tekens lang zijn")

    if not re.search(r'\d', password):
        errors.append("Wachtwoord moet minimaal 1 cijfer bevatten")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Wachtwoord moet minimaal 1 speciaal teken bevatten")
    if not re.search(r'[A-Z]', password):
        errors.append("Wachtwoord moet minimaal 1 hoofdletter bevatten")

    return errors


def change_user_password(user_id, old_password, new_password):
    try:
        # Validate new password
        validation_errors = validate_password(new_password)
        if validation_errors:
            return {'success': False, 'errors': validation_errors}, 400

        with Database() as db:
            # Get user
            db.execute_query("SELECT password FROM users WHERE userID = %s", (user_id,))
            user = db.fetch_one()

            if not user:
                return {'success': False, 'error': 'Gebruiker niet gevonden'}, 404

            # Verify old password
            if not verify_password(old_password, user['password']):
                return {'success': False, 'error': 'Hudig wachtwoord is onjuist'}, 401

            # Hash new password
            hashed_password = generate_password_hash(new_password)

            # Update password
            db.execute_query(
                "UPDATE users SET password = %s WHERE userID = %s",
                (hashed_password, user_id)
            )
            db.commit()
            return {'success': True, 'message': 'Wachtwoord succesvol gewijzigd'}, 200

    except Exception as e:
        print(f"Database error in change_user_password: {e}")
        return {'success': False, 'error': str(e)}, 500


def first_name_check_validity(first_name):
    """
    Check if first name is valid.

    :param first_name: String containing first name
    :return: Boolean confirming if first name is valid or not
    """
    if len(first_name) <= 30:
        return True
    return False


def name_particle_check_validity(name_particle):
    """
    Check if name particle is valid.

    :param name_particle: String containing name particle
    :return: Boolean confirming if first name particle is valid or not
    """
    if len(name_particle) <= 10:
        return True
    return False


def last_name_check_validity(last_name):
    """
    Check if last name is valid.

    :param last_name: String containing last name
    :return: Boolean confirming if last name is valid or not
    """
    if len(last_name) <= 30:
        return True
    return False


def phone_number_check_validity(phone_number):
    """
    Check if phone number is valid.

    :param phone_number: String containing phone number
    :return: Boolean confirming if phone number is valid or not
    """
    if re.match(r"^\+31\d{9}$|^\+32\d{8,9}$|^\+44\d{7,10}$|^\+1\d{10}$|^\+49\d{6,13}$", phone_number):
        return True
    return False


def phone_number_format(phone_number):
    """
    Formats phone number by removing everything except numbers and the '+' character.

    :param phone_number: String containing phone number
    :return: String of formated phone number
    """
    phone_number = re.sub(r"[^0-9+]+", '', phone_number)
    return phone_number


def edit_user_info_db(data, user_id):
    """
    Writes the user information to the database.

    :param data: Dictionary containing the user information
    :param user_id: Integer identifying the user
    :return: Success status, HTTP response status code
    """
    allowed_columns = {"email", "password", "adress", "zipcode", "country", "firstName",
                       "nameParticle", "lastName", "phonenumber", "bankaccount"}

    valid_data = {key: val for key, val in data.items() if val not in [None, "", " "] and key in allowed_columns}
    if not valid_data:
        return {"success": False, "error": "No valid data"}, 400

    if "password" in valid_data and valid_data["password"]:
        valid_data["password"] = generate_password_hash(valid_data["password"])

    if "firstName" in valid_data:
        first_name = valid_data.get("firstName")
        first_name = first_name.strip()
        if first_name_check_validity(first_name):
            valid_data.update({"firstName": first_name})
        else:
            return {"success": False, "error": "Invalid first name"}, 400

    if "nameParticle" in valid_data:
        name_particle = valid_data.get("nameParticle")
        name_particle = name_particle.strip()
        if name_particle_check_validity(name_particle):
            valid_data.update({"nameParticle": name_particle})
        else:
            return {"success": False, "error": "Invalid name particle"}, 400

    if "lastName" in valid_data:
        last_name = valid_data.get("lastName")
        last_name = last_name.strip()
        if last_name_check_validity(last_name):
            valid_data.update({"lastName": last_name})
        else:
            return {"success": False, "error": "Invalid last name"}, 400

    if "phonenumber" in valid_data:
        phone_number = valid_data.get("phonenumber")
        phone_number = phone_number_format(phone_number)
        if phone_number_check_validity(phone_number):
            valid_data.update({"phonenumber": phone_number})
        else:
            return {"success": False, "error": "Invalid phone number"}, 400

    columns = list(valid_data.keys())
    set_column = ", ".join([f"{column} = %s" for column in columns])

    sql = f"UPDATE users SET {set_column} WHERE userID = %s"
    val = list(valid_data.values()) + [user_id]

    try:
        with Database() as DB:
            DB.execute_query(sql, val)
            DB.commit()

        return {"success": True}, 200
    except Exception as e:
        return {"success": False, "error": str(e)}, 400
