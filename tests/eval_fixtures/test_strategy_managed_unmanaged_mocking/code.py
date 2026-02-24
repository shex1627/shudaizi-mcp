"""Tests for a user registration service."""

from unittest.mock import MagicMock, patch, AsyncMock
import pytest


# ── Production code (simplified) ─────────────────────────────────


class EmailValidator:
    """Internal helper — validates email format."""

    def is_valid(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]


class UserRepository:
    """Stores users in PostgreSQL."""

    def __init__(self, db_connection):
        self._conn = db_connection

    def save(self, user_data: dict) -> int:
        cursor = self._conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s) RETURNING id",
            (user_data["email"], user_data["name"], user_data["password_hash"]),
        )
        self._conn.commit()
        return cursor.fetchone()[0]

    def find_by_email(self, email: str) -> dict | None:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cursor.fetchone()
        return dict(row) if row else None


class SendGridClient:
    """Third-party email API."""

    def __init__(self, api_key: str):
        self._api_key = api_key

    def send_email(self, to: str, subject: str, body: str) -> dict:
        # Calls https://api.sendgrid.com/v3/mail/send
        ...


class EventPublisher:
    """Publishes events to RabbitMQ."""

    def __init__(self, connection_url: str):
        self._url = connection_url

    def publish(self, event_type: str, payload: dict) -> None:
        # Sends message to RabbitMQ exchange
        ...


class UserRegistrationService:
    def __init__(self, repo: UserRepository, email_client: SendGridClient,
                 publisher: EventPublisher, validator: EmailValidator):
        self._repo = repo
        self._email_client = email_client
        self._publisher = publisher
        self._validator = validator

    def register(self, email: str, name: str, password_hash: str) -> dict:
        if not self._validator.is_valid(email):
            raise ValueError("Invalid email")
        if self._repo.find_by_email(email):
            raise ValueError("Email already registered")
        user_id = self._repo.save({"email": email, "name": name, "password_hash": password_hash})
        self._email_client.send_email(email, "Welcome!", f"Hi {name}, welcome aboard!")
        self._publisher.publish("user.registered", {"user_id": user_id, "email": email})
        return {"id": user_id, "email": email, "name": name}


# ── Test suite ───────────────────────────────────────────────────


class TestUserRegistration:
    """Tests for the user registration flow."""

    def setup_method(self):
        # Database repository
        self.mock_repo = MagicMock(spec=UserRepository)
        self.mock_repo.save.return_value = 42
        self.mock_repo.find_by_email.return_value = None

        # Email validator
        self.mock_validator = MagicMock(spec=EmailValidator)
        self.mock_validator.is_valid.return_value = True

        # SendGrid email client
        self.real_sendgrid = SendGridClient(api_key="SG.real-api-key-here")

        # RabbitMQ event publisher
        self.real_publisher = EventPublisher(connection_url="amqp://prod-rabbit:5672")

        self.service = UserRegistrationService(
            repo=self.mock_repo,
            email_client=self.real_sendgrid,
            publisher=self.real_publisher,
            validator=self.mock_validator,
        )

    def test_successful_registration(self):
        result = self.service.register("alice@example.com", "Alice", "hashed_pw")
        assert result["id"] == 42
        assert result["email"] == "alice@example.com"
        self.mock_repo.save.assert_called_once()

    def test_duplicate_email_raises(self):
        self.mock_repo.find_by_email.return_value = {"id": 1, "email": "alice@example.com"}
        with pytest.raises(ValueError, match="already registered"):
            self.service.register("alice@example.com", "Alice", "hashed_pw")

    def test_invalid_email_raises(self):
        self.mock_validator.is_valid.return_value = False
        with pytest.raises(ValueError, match="Invalid email"):
            self.service.register("not-an-email", "Bob", "hashed_pw")
        self.mock_repo.save.assert_not_called()

    def test_welcome_email_sent(self):
        self.service.register("bob@example.com", "Bob", "hashed_pw")

    def test_event_published_on_registration(self):
        self.service.register("carol@example.com", "Carol", "hashed_pw")

    def test_registration_saves_correct_data(self):
        self.service.register("dave@example.com", "Dave", "hashed_pw")
        self.mock_repo.save.assert_called_once_with({
            "email": "dave@example.com",
            "name": "Dave",
            "password_hash": "hashed_pw",
        })

    def test_validator_called_before_save(self):
        self.service.register("eve@example.com", "Eve", "hashed_pw")
        self.mock_validator.is_valid.assert_called_once_with("eve@example.com")
        self.mock_repo.save.assert_called_once()
