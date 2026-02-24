"""Async notification service for sending alerts and digests."""

import asyncio
import time
import requests


async def send_notification(user_id: int, message: str) -> bool:
    """Send a push notification to the user."""
    # Fetch user's device token
    response = requests.get(f"http://internal-api/users/{user_id}/devices")
    if response.status_code != 200:
        return False

    devices = response.json()

    for device in devices:
        # Send to each device
        result = requests.post(
            "http://push-service/send",
            json={"token": device["token"], "message": message},
        )
        if result.status_code != 200:
            print(f"Failed to notify device {device['id']}")

    return True


async def send_bulk_notifications(user_ids: list[int], message: str):
    """Send notifications to multiple users."""
    for user_id in user_ids:
        await send_notification(user_id, message)
        time.sleep(0.1)  # Rate limiting
