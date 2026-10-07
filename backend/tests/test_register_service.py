from unittest.mock import MagicMock, patch
from services import auth_service

def test_validate_registration_missing_fields():
    error = auth_service.validate_registration({})
    assert error == "Email en wachtwoord zijn vereist."

def test_validate_registration_invalid_email():
    error = auth_service.validate_registration({"email": "bademail", "password": "Password1"})
    assert error == "Voer een geldig e-mailadres in."

def test_validate_registration_weak_password():
    error = auth_service.validate_registration({"email": "user@example.com", "password": "short"})
    assert error == "Minimaal 8 tekens vereist voor wachtwoord."

def test_register_user_duplicate_email():
    mock_db = MagicMock()
    mock_db.fetch_one.return_value = {"count": 1}
    mock_db_context = MagicMock()
    mock_db_context.__enter__.return_value = mock_db
    mock_db_context.__exit__.return_value = None

    with patch("services.auth_service.Database", return_value=mock_db_context):
        result, status = auth_service.register_user({
            "email": "user@example.com",
            "password": "Password123"
        })

    assert status == 409
    assert result["error"] == "Er bestaat al een account met dit e-mailadres."
    mock_db.execute_query.assert_called_once_with("SELECT COUNT(*) as count FROM users WHERE email = %s", ("user@example.com",))

def test_register_user_success():
    mock_db = MagicMock()
    mock_db.fetch_one.return_value = {"count": 0}
    mock_db_context = MagicMock()
    mock_db_context.__enter__.return_value = mock_db
    mock_db_context.__exit__.return_value = None

    with patch("services.auth_service.Database", return_value=mock_db_context):
        result, status = auth_service.register_user({
            "email": "user@example.com",
            "password": "Password123",
            "firstName": "Test",
            "lastName": "User",
            "zipcode": "1234AB",
            "country": "NL"
        })

    assert status == 201
    assert result["message"] == "User registered successfully"
    assert mock_db.execute_query.call_count == 2
    mock_db.commit.assert_called_once()