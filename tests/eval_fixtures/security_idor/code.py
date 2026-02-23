"""Order management API — vulnerable to IDOR."""

from flask import Flask, request, jsonify, g

app = Flask(__name__)


def get_db():
    import sqlite3
    return sqlite3.connect("app.db")


def get_current_user_id() -> int:
    """Extract authenticated user ID from session/token."""
    return g.user_id


@app.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    """Fetch order details by ID."""
    db = get_db()
    cursor = db.execute(
        "SELECT id, user_id, total, status, items FROM orders WHERE id = ?",
        (order_id,),
    )
    order = cursor.fetchone()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return jsonify({
        "id": order[0],
        "user_id": order[1],
        "total": order[2],
        "status": order[3],
        "items": order[4],
    })


@app.route("/api/orders/<int:order_id>", methods=["DELETE"])
def cancel_order(order_id):
    """Cancel an order by ID."""
    db = get_db()
    db.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
    db.commit()
    return jsonify({"message": "Order cancelled"})
