I need to add tests for our payment processing service. Here's the class.
Can you write a comprehensive test suite? Use pytest.

```python
"""Payment processing service."""

import stripe
from sqlalchemy.orm import Session

from app.models import Payment, User
from app.events import EventBus


class PaymentService:
    def __init__(self, db: Session, event_bus: EventBus):
        self.db = db
        self.event_bus = event_bus

    def charge(self, user_id: int, amount_cents: int, currency: str = "usd") -> Payment:
        user = self.db.query(User).get(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        if amount_cents <= 0:
            raise ValueError("Amount must be positive")

        stripe_charge = stripe.Charge.create(
            amount=amount_cents,
            currency=currency,
            customer=user.stripe_customer_id,
        )

        payment = Payment(
            user_id=user_id,
            amount_cents=amount_cents,
            stripe_charge_id=stripe_charge.id,
            status="completed",
        )
        self.db.add(payment)
        self.db.commit()

        self.event_bus.publish("payment.completed", {
            "payment_id": payment.id,
            "user_id": user_id,
            "amount": amount_cents,
        })

        return payment

    def refund(self, payment_id: int) -> Payment:
        payment = self.db.query(Payment).get(payment_id)
        stripe.Refund.create(charge=payment.stripe_charge_id)
        payment.status = "refunded"
        self.db.commit()
        self.event_bus.publish("payment.refunded", {"payment_id": payment_id})
        return payment
```

I want good coverage — happy paths, edge cases, error scenarios.
