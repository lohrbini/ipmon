import socket
import requests
import os
import json
import time
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables for configuration
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY", "your_pushover_user_key")
PUSHOVER_API_TOKEN = os.getenv("PUSHOVER_API_TOKEN", "your_pushover_api_token")
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "your_ntfy_topic")
NTFY_SERVER_URL = os.getenv("NTFY_SERVER_URL", "https://ntfy.yourdomain.com")
NTFY_USERNAME = os.getenv("NTFY_USERNAME", "your_ntfy_username")
NTFY_PASSWORD = os.getenv("NTFY_PASSWORD", "your_ntfy_password")

# File to store the previous IPv6 addresses
IPV6_FILE = "ipv6_addresses.json"

# Domains to monitor for IPv6 changes (can be set as comma-separated via env var)
DOMAINS_TO_MONITOR = os.getenv("DOMAINS_TO_MONITOR", "example.com,ipv6.google.com").split(",")

# Sleep interval in seconds (default: 600 seconds = 10 minutes)
SLEEP_INTERVAL = int(os.getenv("SLEEP_INTERVAL", "600"))

# Get the IPv6 address for a domain
def get_ipv6_address(domain):
    try:
        logging.info(f"Getting IPv6 address for domain: {domain}")
        result = socket.getaddrinfo(domain, None, socket.AF_INET6)
        ipv6_address = result[0][4][0]  # Extract the IPv6 address
        logging.info(f"Found IPv6 address for {domain}: {ipv6_address}")
    except Exception as e:
        logging.error(f"Error getting IPv6 address for {domain}: {e}")
        ipv6_address = None
    return ipv6_address

# Send a notification via Pushover
def send_pushover_notification(message):
    logging.info(f"Sending Pushover notification: {message}")
    data = {
        "user": PUSHOVER_USER_KEY,      # Required: User key
        "token": PUSHOVER_API_TOKEN,    # Required: API token
        "message": message,             # Required: Message text
        "title": "IPv6 Address Change", # Optional: Message title
        "priority": 0                   # Optional: Priority (0 is normal)
    }
    try:
        response = requests.post(PUSHOVER_API_URL, data=data)
        response.raise_for_status()  # Raises a RequestException for non-2xx responses
        logging.info(f"Pushover notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Pushover notification: {e}")

# Send a notification to ntfy (using requests to make HTTP POST)
def send_ntfy_notification(message):
    logging.info(f"Sending ntfy notification: {message}")
    try:
        headers = {
            "Title": "IPv6 Change Notification"
        }
        # HTTP Basic Authentication for private ntfy instance
        response = requests.post(
            f"{NTFY_SERVER_URL}/{NTFY_TOPIC}",
            data=message,
            headers=headers,
            auth=(NTFY_USERNAME, NTFY_PASSWORD)
        )
        response.raise_for_status()  # Raise an error if the request failed
        logging.info(f"ntfy notification sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send ntfy notification: {e}")

# Load stored IPv6 addresses from file
def load_stored_ipv6_addresses():
    if os.path.exists(IPV6_FILE):
        logging.info("Loading stored IPv6 addresses from file.")
        with open(IPV6_FILE, "r") as file:
            return json.load(file)
    logging.info("No stored IPv6 addresses found. Starting fresh.")
    return {}

# Save the current IPv6 addresses to file
def save_ipv6_addresses(ipv6_addresses):
    logging.info("Saving current IPv6 addresses to file.")
    with open(IPV6_FILE, "w") as file:
        json.dump(ipv6_addresses, file)

# Monitor for IPv6 address changes
def monitor_ipv6_addresses():
    logging.info("Starting to monitor IPv6 addresses...")
    
    # Load the previously stored IPv6 addresses
    stored_ipv6_addresses = load_stored_ipv6_addresses()

    # Dictionary to hold the current IPv6 addresses
    current_ipv6_addresses = {}

    # Check the IPv6 address for each domain
    for domain in DOMAINS_TO_MONITOR:
        current_ipv6 = get_ipv6_address(domain.strip())
        if not current_ipv6:
            logging.warning(f"Could not obtain IPv6 address for {domain}. Skipping.")
            continue

        current_ipv6_addresses[domain] = current_ipv6
        last_ipv6 = stored_ipv6_addresses.get(domain)

        # If the IPv6 address has changed, send notifications
        if current_ipv6 != last_ipv6:
            message = f"IPv6 address for {domain} has changed to {current_ipv6}"
            logging.info(f"IPv6 address changed: {message}")

            # Send notifications via ntfy and Pushover
            send_ntfy_notification(message)
            send_pushover_notification(message)

    # Save the current IPv6 addresses for future comparison
    save_ipv6_addresses(current_ipv6_addresses)

# Main loop
if __name__ == "__main__":
    logging.info("Starting IPv6 monitor script.")
    while True:
        monitor_ipv6_addresses()
        logging.info(f"Sleeping for {SLEEP_INTERVAL} seconds...")
        time.sleep(SLEEP_INTERVAL)
