"""Shopping cart service for managing user carts."""

from datetime import datetime


class ShoppingCart:
    def __init__(self, db):
        self.db = db

    def get_total(self, cart_id: int) -> float:
        """Get the cart total. Also applies any pending discounts as a side effect."""
        cart = self.db.execute(
            "SELECT * FROM carts WHERE id = ?", (cart_id,)
        ).fetchone()

        # Apply pending discounts (mutation!)
        discounts = self.db.execute(
            "SELECT * FROM pending_discounts WHERE cart_id = ? AND applied = 0",
            (cart_id,),
        ).fetchall()

        for discount in discounts:
            self.db.execute(
                "UPDATE pending_discounts SET applied = 1 WHERE id = ?",
                (discount["id"],),
            )
            self.db.execute(
                "UPDATE carts SET discount_total = discount_total + ? WHERE id = ?",
                (discount["amount"], cart_id),
            )
        self.db.commit()

        # Now calculate total
        items = self.db.execute(
            "SELECT price, quantity FROM cart_items WHERE cart_id = ?", (cart_id,)
        ).fetchall()
        subtotal = sum(item["price"] * item["quantity"] for item in items)
        return subtotal - cart["discount_total"]

    def remove_item(self, cart_id: int, item_id: int) -> dict:
        """Remove an item from the cart. Returns the updated cart summary."""
        self.db.execute(
            "DELETE FROM cart_items WHERE cart_id = ? AND id = ?",
            (cart_id, item_id),
        )
        self.db.commit()

        # Also return the full cart state (query + command mixed)
        items = self.db.execute(
            "SELECT * FROM cart_items WHERE cart_id = ?", (cart_id,)
        ).fetchall()
        total = self.get_total(cart_id)  # This triggers discount application again!

        return {
            "cart_id": cart_id,
            "items": [dict(i) for i in items],
            "total": total,
            "updated_at": datetime.now().isoformat(),
        }
