"""Message queue consumer for processing async jobs."""

import json
import requests


class MessageConsumer:
    def __init__(self, queue_url: str, handler_url: str):
        self.queue_url = queue_url
        self.handler_url = handler_url

    def process_message(self, message: dict) -> bool:
        """Process a single message by forwarding to the handler service."""
        max_retries = 10
        attempt = 0

        while attempt < max_retries:
            try:
                response = requests.post(
                    self.handler_url,
                    json=message,
                )
                if response.status_code == 200:
                    return True
                attempt += 1
            except requests.ConnectionError:
                attempt += 1

        return False

    def consume(self):
        """Main consume loop — polls the queue and processes messages."""
        while True:
            response = requests.get(self.queue_url)
            if response.status_code != 200:
                continue

            messages = response.json().get("messages", [])
            for msg in messages:
                success = self.process_message(msg)
                if not success:
                    # Just retry the whole message
                    self.process_message(msg)
