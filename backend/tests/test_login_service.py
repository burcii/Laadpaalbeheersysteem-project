import jwt
from unittest.mock import MagicMock, patch
from services import auth_service

def test_login_user_missing_fields():
    result, status = auth_service.login_user("", "")
    assert status == 400
    assert result["error"] == "Email and password are required"

def test_login_user_invalid_credentials():
    mock_db = MagicMock()
    mock_db.fetch_one.return_value = None
    mock_db_context = MagicMock()
    mock_db_context.__enter__.return_value = mock_db
    mock_db_context.__exit__.return_value = None

    with patch("services.auth_service.Database", return_value=mock_db_context):
        result, status = auth_service.login_user("user@example.com", "wrongpass")

    assert status == 401
    assert result["error"] == "Ongeldige inloggegevens"

def test_login_user_success():
    hashed_password = auth_service.generate_password_hash("Password123")
    mock_db = MagicMock()
    mock_db.fetch_one.return_value = {"userID": 42, "password": hashed_password}
    mock_db_context = MagicMock()
    mock_db_context.__enter__.return_value = mock_db
    mock_db_context.__exit__.return_value = None

    with patch("services.auth_service.Database", return_value=mock_db_context):
        result, status = auth_service.login_user("user@example.com", "Password123")

    assert status == 200
    assert "token" in result

    decoded = jwt.decode(result["token"], auth_service.config.SECRET_KEY, algorithms=["HS256"])
    assert decoded["user_id"] == 42
    