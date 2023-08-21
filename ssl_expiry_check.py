import requests
import datetime
import os

# Read domains from a file (each line is a domain)
with open('domain_list.txt', 'r') as file:
    domains = file.read().splitlines()

# Iterate through domains
for domain in domains:
    response = requests.get(f'https://api.ssllabs.com/api/v3/analyze?host={domain}')
    data = response.json()

    if data['status'] == 'READY':
        expiry_date_str = data['endpoints'][0]['details']['cert']['notAfter']
        expiry_date = datetime.datetime.strptime(expiry_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        days_remaining = (expiry_date - datetime.datetime.now()).days

        if days_remaining < 30:
            message = (
                f"SSL Expiry Alert\n"
                f"   * Domain: {domain}\n"
                f"   * Warning: The SSL certificate for {domain} will expire in {days_remaining} days."
            )

            slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']
            payload = {"text": message}
            requests.post(slack_webhook_url, json=payload)
