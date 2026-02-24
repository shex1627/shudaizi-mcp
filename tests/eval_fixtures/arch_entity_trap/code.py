"""Microservice architecture for an e-commerce platform.

Five services handling users, products, orders, payments, and shipping.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


# ── Shared event bus (simplified) ────────────────────────────────


class EventBus:
    def __init__(self):
        self._handlers: dict[str, list] = {}

    def subscribe(self, event_type: str, handler):
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event_type: str, payload: dict):
        for handler in self._handlers.get(event_type, []):
            handler(payload)


bus = EventBus()


# ── User Service ─────────────────────────────────────────────────


@dataclass
class User:
    id: str
    email: str
    name: str
    address: str
    created_at: datetime = field(default_factory=datetime.utcnow)


class UserService:
    """Manages the User entity — CRUD operations on users."""

    def __init__(self):
        self._users: dict[str, User] = {}

    def create_user(self, email: str, name: str, address: str) -> User:
        user = User(id=str(uuid.uuid4()), email=email, name=name, address=address)
        self._users[user.id] = user
        bus.publish("user.created", {"user_id": user.id, "email": email})
        return user

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def update_address(self, user_id: str, new_address: str) -> User | None:
        user = self._users.get(user_id)
        if user:
            user.address = new_address
            bus.publish("user.address_changed", {"user_id": user_id, "address": new_address})
        return user

    def list_users(self) -> list[User]:
        return list(self._users.values())


# ── Product Service ──────────────────────────────────────────────


@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int
    category: str


class ProductService:
    """Manages the Product entity — CRUD and stock operations."""

    def __init__(self):
        self._products: dict[str, Product] = {}

    def create_product(self, name: str, price: float, stock: int, category: str) -> Product:
        product = Product(id=str(uuid.uuid4()), name=name, price=price, stock=stock, category=category)
        self._products[product.id] = product
        return product

    def get_product(self, product_id: str) -> Product | None:
        return self._products.get(product_id)

    def update_stock(self, product_id: str, delta: int) -> Product | None:
        product = self._products.get(product_id)
        if product:
            product.stock += delta
        return product

    def list_by_category(self, category: str) -> list[Product]:
        return [p for p in self._products.values() if p.category == category]


# ── Order Service ────────────────────────────────────────────────


@dataclass
class OrderLine:
    product_id: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    id: str
    user_id: str
    lines: list[OrderLine]
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def total(self) -> float:
        return sum(line.quantity * line.unit_price for line in self.lines)


class OrderService:
    """Manages the Order entity — create, cancel, list by user."""

    def __init__(self, product_service: ProductService):
        self._orders: dict[str, Order] = {}
        self._product_service = product_service

    def create_order(self, user_id: str, items: list[dict]) -> Order:
        lines = []
        for item in items:
            product = self._product_service.get_product(item["product_id"])
            if not product or product.stock < item["quantity"]:
                raise ValueError(f"Insufficient stock for {item['product_id']}")
            lines.append(OrderLine(
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=product.price,
            ))
        order = Order(id=str(uuid.uuid4()), user_id=user_id, lines=lines)
        self._orders[order.id] = order

        # Decrement stock directly
        for line in lines:
            self._product_service.update_stock(line.product_id, -line.quantity)

        bus.publish("order.created", {"order_id": order.id, "user_id": user_id, "total": order.total})
        return order

    def cancel_order(self, order_id: str) -> Order | None:
        order = self._orders.get(order_id)
        if order and order.status == "pending":
            order.status = "cancelled"
            for line in order.lines:
                self._product_service.update_stock(line.product_id, line.quantity)
            bus.publish("order.cancelled", {"order_id": order_id})
        return order

    def list_by_user(self, user_id: str) -> list[Order]:
        return [o for o in self._orders.values() if o.user_id == user_id]


# ── Payment Service ──────────────────────────────────────────────


@dataclass
class Payment:
    id: str
    order_id: str
    amount: float
    status: str = "pending"


class PaymentService:
    """Manages the Payment entity — process and refund payments."""

    def __init__(self):
        self._payments: dict[str, Payment] = {}

    def process_payment(self, order_id: str, amount: float) -> Payment:
        payment = Payment(id=str(uuid.uuid4()), order_id=order_id, amount=amount)
        # Simulate payment gateway call
        payment.status = "completed"
        self._payments[payment.id] = payment
        bus.publish("payment.completed", {"payment_id": payment.id, "order_id": order_id})
        return payment

    def refund(self, payment_id: str) -> Payment | None:
        payment = self._payments.get(payment_id)
        if payment and payment.status == "completed":
            payment.status = "refunded"
            bus.publish("payment.refunded", {"payment_id": payment_id, "order_id": payment.order_id})
        return payment

    def get_by_order(self, order_id: str) -> list[Payment]:
        return [p for p in self._payments.values() if p.order_id == order_id]


# ── Shipping Service ─────────────────────────────────────────────


@dataclass
class Shipment:
    id: str
    order_id: str
    address: str
    status: str = "preparing"


class ShippingService:
    """Manages the Shipment entity — create and track shipments."""

    def __init__(self, user_service: UserService):
        self._shipments: dict[str, Shipment] = {}
        self._user_service = user_service

    def create_shipment(self, order_id: str, user_id: str) -> Shipment:
        user = self._user_service.get_user(user_id)
        address = user.address if user else "unknown"
        shipment = Shipment(id=str(uuid.uuid4()), order_id=order_id, address=address)
        self._shipments[shipment.id] = shipment
        return shipment

    def mark_shipped(self, shipment_id: str) -> Shipment | None:
        shipment = self._shipments.get(shipment_id)
        if shipment:
            shipment.status = "shipped"
            bus.publish("shipment.shipped", {"shipment_id": shipment_id, "order_id": shipment.order_id})
        return shipment

    def get_by_order(self, order_id: str) -> list[Shipment]:
        return [s for s in self._shipments.values() if s.order_id == order_id]
