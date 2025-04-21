import yaml
import requests
import time
from collections import defaultdict

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')  # Default to GET if method is missing
    headers = endpoint.get('headers', None)
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=yaml.safe_load(body) if body else None, timeout=5)
        elapsed_time = time.time() - start_time

        # Endpoint is considered UP only if status is 2xx AND response is under 500ms
        if 200 <= response.status_code < 300 and elapsed_time <= 0.5:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            # Strip port number if present in domain
            domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            # Drop decimal part of availability percentage as per spec
            availability = int(100 * stats["up"] / stats["total"])
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
