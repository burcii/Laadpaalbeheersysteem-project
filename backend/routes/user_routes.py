from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.edit_user_service import change_user_password
from services.user_service import (
    add_user_to_db,
    update_user_in_db,
    delete_user_from_db,
    get_all_users_from_db,
    toggle_user_block_status,
    get_user_role_from_db,
    get_user_details_from_db
)

user_bp = Blueprint("user", __name__)

@user_bp.route('/get_role/<int:user_id>', methods=['GET'])
def get_role(user_id):
    if not user_id:
        return jsonify({'success': False, 'error': 'Missing user_id'}), 400

    try:
        result, status = get_user_role_from_db(user_id)
        return jsonify(result), status
    except Exception as e:
        print("Error fetching user role:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/get_user_details/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    if not user_id:
        return jsonify({'success': False, 'error': 'Missing user_id'}), 400

    try:
        result, status = get_user_details_from_db(user_id)
        return jsonify(result), status
    except Exception as e:
        print("Error fetching user details:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/add_user', methods=['POST'])
def add_user():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        pass_number = request.form.get('pass_number')

        if not name or not email or not pass_number:
            return jsonify({'error': 'Missing required fields'}), 400

        new_user = add_user_to_db(name, email, phone, pass_number)
        if new_user:
            return jsonify({'success': True, 'user': new_user}), 201
        return jsonify({'error': 'Failed to add user'}), 500
    except Exception as e:
        print(f"Error in add_user endpoint: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@user_bp.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        pass_number = request.form.get('pass_number')

        if not name or not email or not pass_number:
            return jsonify({'error': 'Verplichte velden ontbreken'}), 400

        updated_user = update_user_in_db(user_id, name, email, phone, pass_number)
        if updated_user:
            return jsonify({'success': True, 'user': updated_user}), 200
        return jsonify({'error': 'De gebruiker kan niet worden aangepast.'}), 500
    except Exception as e:
        print(f"Error in update_user endpoint: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@user_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        result, status = delete_user_from_db(user_id)
        return jsonify(result), status
    except Exception as e:
        print("Fout bij het verwijderen van gebruiker:", e)
        return jsonify({'succes': False, 'error': str(e)}), 500

@user_bp.route('/get_users', methods=['GET'])
def get_users():
    try:
        result, status = get_all_users_from_db()
        return jsonify(result), status
    except Exception as e:
        print("Fout bij het ophalen van gebruikers:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@user_bp.route('/toggle_block_user/<int:user_id>', methods=['PATCH'])
def toggle_block_user(user_id):
    try:
        result, status = toggle_user_block_status(user_id)
        return jsonify(result), status
    except Exception as e:
        print("Fout bij het blokkeren van gebruiker:", e)
        return jsonify({'success': False, 'error': str(e)}), 500
    
@user_bp.route('/change_password', methods=['POST'])
def change_password():
    try:
        user_id = request.form.get('user_id')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')

        if not user_id or not old_password or not new_password:
            return jsonify({'error': 'Verplichte velden ontbreken'}), 400

        result, status = change_user_password(int(user_id), old_password, new_password)
        return jsonify(result), status
    except Exception as e:
        print(f"Error in change_password endpoint: {e}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@user_bp.route('/get_user_pages/<int:user_id>', methods=['GET'])
def get_user_pages(user_id):
    try:
        user_role = get_user_role_from_db(user_id)
        
        pages = {
            'admin': [{'name': 'Dashboard', 'link': '/'}, {'name': 'Laadpaalbeheer', 'link': '/laadpaalbeheer'}, {'name': 'Sessies', 'link': '/sessies'}, {'name': 'Locaties', 'link': '/locaties'}, {'name': 'Gebruikers', 'link': '/usermanagement'}, {'name': 'Bewerk Account', 'link': '/edit_user'}],
            'management': [{'name': 'Dashboard', 'link': '/'}, {'name': 'Sessies', 'link': '/sessies'}, {'name': 'Gebruikers', 'link': '/usermanagement'}, {'name': 'Bewerk Account', 'link': '/edit_user'}],
            'user': [{'name': 'Dashboard', 'link': '/'}, {'name': 'Sessies', 'link': '/sessies'}, {'name': 'Bewerk Account', 'link': '/edit_user'}]
        }

        return jsonify({'success': True, 'pages': pages[user_role[0]['role']]}), 200
    except Exception as e:
        print("Fout bij het ophalen van gebruikerspagina's:", e)
        return jsonify({'success': False, 'error': str(e)}), 500