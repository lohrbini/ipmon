# IPv6 Monitor

This project monitors specified domains for changes to their IPv6 addresses and sends notifications via **ntfy** and **Pushover** whenever a change is detected.

## Requirements

- Python 3.11 or later
- Docker (for containerization)

## Libraries Used

- **ntfy**: A notification service to send messages.
- **python-pushover**: A Python client for the Pushover API.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/lohrbini/ipmon.git
    cd ipmon
    ```

2. **Build the Docker image**:
    ```bash
    docker build -t ipmon .
    ```

## Configuration

You can configure the script using environment variables. Here are the required and optional variables:

| Variable                    | Description                                                   | Default                        |
|-----------------------------|---------------------------------------------------------------|--------------------------------|
| `PUSHOVER_USER_KEY`         | Your Pushover user key                                       | `your_pushover_user_key`      |
| `PUSHOVER_API_TOKEN`        | Your Pushover API token                                      | `your_pushover_api_token`     |
| `NTFY_TOPIC`                | The topic to send notifications to on ntfy                   | `your_ntfy_topic`             |
| `NTFY_SERVER_URL`           | The URL of your ntfy server (should include HTTPS)          | `https://ntfy.yourdomain.com` |
| `NTFY_USERNAME`             | Your ntfy username (if applicable)                           | `your_ntfy_username`          |
| `NTFY_PASSWORD`             | Your ntfy password (if applicable)                           | `your_ntfy_password`          |
| `DOMAINS_TO_MONITOR`       | Comma-separated list of domains to monitor                   | `example.com,ipv6.google.com` |
| `SLEEP_INTERVAL`            | Time interval (in seconds) to wait between checks           | `600` (10 minutes)            |

## Running the Application

To run the application in a Docker container, use the following command, replacing the environment variables with your own values:

```bash
docker run -d \
  -e PUSHOVER_USER_KEY="your_valid_pushover_user_key" \
  -e PUSHOVER_API_TOKEN="your_valid_pushover_api_token" \
  -e NTFY_SERVER_URL="https://ntfy.yourdomain.com" \
  -e NTFY_TOPIC="your_ntfy_topic" \
  -e NTFY_USERNAME="your_ntfy_username" \
  -e NTFY_PASSWORD="your_ntfy_password" \
  -e DOMAINS_TO_MONITOR="example.com,ipv6.google.com" \
  -e SLEEP_INTERVAL=600 \
  ipmon
```

