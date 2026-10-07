import os
from database import Database

def get_user_role_from_db(user_id):
    try:
        with Database() as db:
            db.execute_query("SELECT role FROM users WHERE userID = %s", (user_id,))
            row = db.fetch_one()
            if not row:
                return {'success': False, 'error': 'User not found'}, 404
            return {'role': row['role']}, 200
    except Exception as e:
        print(f"Database error in get_user_role_from_db: {e}")
        return {'success': False, 'error': str(e)}, 500

def get_user_details_from_db(user_id):
    try:
        with Database() as db:
            db.execute_query("SELECT firstName, nameParticle, lastName, role FROM users WHERE userID = %s", (user_id,))
            row = db.fetch_one()
            if not row:
                return {'success': False, 'error': 'User not found'}, 404
            
            full_name = f"{row['firstName']} "
            if row['nameParticle']:
                full_name += f"{row['nameParticle']} "
            full_name += f"{row['lastName']} "

            return {'success': True, 'user':{'name': full_name.strip(), 'role': row['role']}}, 200
    except Exception as e:
        print(f"Database error in get_user_details_from_db: {e}")
        return {'success': False, 'error': str(e)}, 500

def add_user_to_db(name, email, phone, pass_number):
    try:
        with Database() as db:
            insert_query = """
                INSERT INTO unregisteredUsers (name, email, phone, pass_number, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            db.execute_query(insert_query, (name, email, phone, pass_number, 'Actief'))
            db.commit()

            user_id = db.mycursor.lastrowid
            db.execute_query("SELECT * FROM unregisteredUsers WHERE id = %s", (user_id,))
            return db.fetch_one()
    except Exception as e:
        print(f"Database error in add_user_to_db: {e}")
        import traceback; traceback.print_exc()
        return None

def update_user_in_db(user_id, name, email, phone, pass_number):
    try:
        with Database() as db:
            update_query = """
                UPDATE unregisteredUsers
                SET name = %s, email = %s, phone = %s, pass_number = %s
                WHERE id = %s
            """
            db.execute_query(update_query, (name, email, phone, pass_number, user_id))
            db.commit()

            db.execute_query("SELECT * FROM unregisteredUsers WHERE id = %s", (user_id,))
            return db.fetch_one()
    except Exception as e:
        print(f"Database error in update_user_in_db: {e}")
        import traceback; traceback.print_exc()
        return None

def delete_user_from_db(user_id):
    try:
        with Database() as db:
            db.execute_query("DELETE FROM unregisteredUsers WHERE id = %s", (user_id,))
            db.commit()
            if db.mycursor.rowcount > 0:
                return {'succes': True, 'message': 'Gebruiker succesvol verwijderd'}, 200
            return {'succes': False, 'error': 'Gebruiker niet gevonden'}, 404
    except Exception as e:
        print(f"Database error in delete_user_from_db: {e}")
        return {'succes': False, 'error': str(e)}, 500

def get_all_users_from_db():
    try:
        with Database() as db:
            db.execute_query("SELECT * FROM unregisteredUsers ORDER BY id DESC")
            users = db.fetch_results()
            return {'success': True, 'users': users}, 200
    except Exception as e:
        print(f"Database error in get_all_users_from_db: {e}")
        return {'success': False, 'error': str(e)}, 500

def toggle_user_block_status(user_id):
    try:
        with Database() as db:
            db.execute_query("SELECT status FROM unregisteredUsers WHERE id = %s", (user_id,))
            current_user = db.fetch_one()
            if not current_user:
                return {'success': False, 'error': 'Gebruiker niet gevonden'}, 404

            new_status = 'Geblokkeerd' if current_user['status'] == 'Actief' else 'Actief'
            db.execute_query("UPDATE unregisteredUsers SET status = %s WHERE id = %s", (new_status, user_id))
            db.commit()

            db.execute_query("SELECT * FROM unregisteredUsers WHERE id = %s", (user_id,))
            updated_user = db.fetch_one()
            return {'success': True, 'user': updated_user}, 200
    except Exception as e:
        print(f"Database error in toggle_user_block_status: {e}")
        return {'success': False, 'error': str(e)}, 500
    