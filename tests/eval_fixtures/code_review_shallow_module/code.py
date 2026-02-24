"""User service layer with repository, service, and controller."""


class UserRepository:
    """Direct database access for users."""

    def __init__(self, db):
        self.db = db

    def find_by_id(self, user_id: int) -> dict | None:
        row = self.db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def find_by_email(self, email: str) -> dict | None:
        row = self.db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

    def save(self, user: dict) -> int:
        cursor = self.db.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (user["name"], user["email"], user["role"]),
        )
        self.db.commit()
        return cursor.lastrowid

    def update(self, user_id: int, data: dict) -> None:
        sets = ", ".join(f"{k} = ?" for k in data)
        self.db.execute(f"UPDATE users SET {sets} WHERE id = ?", (*data.values(), user_id))
        self.db.commit()

    def delete(self, user_id: int) -> None:
        self.db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.db.commit()

    def list_all(self, limit: int = 100, offset: int = 0) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM users LIMIT ? OFFSET ?", (limit, offset)
        ).fetchall()
        return [dict(r) for r in rows]


class UserService:
    """Service layer for user operations."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, user_id: int) -> dict | None:
        return self.repo.find_by_id(user_id)

    def get_user_by_email(self, email: str) -> dict | None:
        return self.repo.find_by_email(email)

    def create_user(self, user: dict) -> int:
        return self.repo.save(user)

    def update_user(self, user_id: int, data: dict) -> None:
        return self.repo.update(user_id, data)

    def delete_user(self, user_id: int) -> None:
        return self.repo.delete(user_id)

    def list_users(self, limit: int = 100, offset: int = 0) -> list[dict]:
        return self.repo.list_all(limit, offset)


class UserController:
    """HTTP controller for user endpoints."""

    def __init__(self, service: UserService):
        self.service = service

    def handle_get_user(self, user_id: int) -> dict:
        return self.service.get_user(user_id)

    def handle_get_user_by_email(self, email: str) -> dict:
        return self.service.get_user_by_email(email)

    def handle_create_user(self, data: dict) -> dict:
        return self.service.create_user(data)

    def handle_update_user(self, user_id: int, data: dict) -> dict:
        return self.service.update_user(user_id, data)

    def handle_delete_user(self, user_id: int) -> dict:
        return self.service.delete_user(user_id)

    def handle_list_users(self, limit: int = 100, offset: int = 0) -> dict:
        return self.service.list_users(limit, offset)
