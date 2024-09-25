# Use Python slim version for a smaller image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the script into the container
COPY ipv6_monitor.py requirements.txt .

# Install required Python libraries
RUN pip install -r requirements.txt

# Run the Python script
CMD ["python", "ipv6_monitor.py"]
