"""Two services sharing the same database connection — distributed monolith."""

import sqlite3

# Shared database connection used by both services
_db = sqlite3.connect("shared_app.db")
_db.row_factory = sqlite3.Row


class OrderService:
    """Handles order lifecycle."""

    def create_order(self, user_id: int, items: list[dict]) -> int:
        total = sum(item["price"] * item["qty"] for item in items)
        cursor = _db.execute(
            "INSERT INTO orders (user_id, total, status) VALUES (?, ?, ?)",
            (user_id, total, "pending"),
        )
        for item in items:
            _db.execute(
                "INSERT INTO order_items (order_id, product_id, qty, price) VALUES (?, ?, ?, ?)",
                (cursor.lastrowid, item["product_id"], item["qty"], item["price"]),
            )
        # Directly update inventory in the same transaction
        for item in items:
            _db.execute(
                "UPDATE products SET stock = stock - ? WHERE id = ?",
                (item["qty"], item["product_id"]),
            )
        _db.commit()
        return cursor.lastrowid

    def get_order(self, order_id: int) -> dict:
        row = _db.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        return dict(row) if row else None


class InventoryService:
    """Manages product inventory."""

    def get_stock(self, product_id: int) -> int:
        row = _db.execute(
            "SELECT stock FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        return row["stock"] if row else 0

    def restock(self, product_id: int, quantity: int) -> None:
        _db.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (quantity, product_id),
        )
        _db.commit()

    def get_low_stock_products(self, threshold: int = 10) -> list[dict]:
        rows = _db.execute(
            "SELECT * FROM products WHERE stock < ?", (threshold,)
        ).fetchall()
        return [dict(r) for r in rows]

    def get_product_with_order_count(self, product_id: int) -> dict:
        """Directly queries order_items table — crossing service boundary."""
        row = _db.execute(
            """SELECT p.*, COUNT(oi.id) as order_count
               FROM products p
               LEFT JOIN order_items oi ON p.id = oi.product_id
               WHERE p.id = ?
               GROUP BY p.id""",
            (product_id,),
        ).fetchone()
        return dict(row) if row else None
