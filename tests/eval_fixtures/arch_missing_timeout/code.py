"""Payment gateway client for processing charges and refunds."""

import httpx
import json


class PaymentGateway:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.Client(
            base_url=base_url,
            headers={"Authorization": f"Bearer {api_key}"},
        )

    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        """Charge a credit card."""
        response = self.client.post(
            "/v1/charges",
            json={"amount": amount, "currency": currency, "source": card_token},
        )
        response.raise_for_status()
        return response.json()

    def refund(self, charge_id: str, amount: float | None = None) -> dict:
        """Refund a charge."""
        payload = {"charge": charge_id}
        if amount:
            payload["amount"] = amount
        response = self.client.post("/v1/refunds", json=payload)
        response.raise_for_status()
        return response.json()

    def get_balance(self) -> dict:
        """Check account balance."""
        response = self.client.get("/v1/balance")
        response.raise_for_status()
        return response.json()

    def list_transactions(self, cursor: str | None = None) -> dict:
        """List recent transactions with pagination."""
        params = {}
        if cursor:
            params["starting_after"] = cursor

        response = self.client.get("/v1/transactions", params=params)
        response.raise_for_status()
        return response.json()
