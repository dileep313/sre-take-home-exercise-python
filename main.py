import yaml
import requests
import time
from collections import defaultdict


def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')  
    headers = endpoint.get('headers', None)
    body = endpoint.get('body', None)

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=yaml.safe_load(body) if body else None, timeout=5)
        elapsed_time = time.time() - start_time

        
        if 200 <= response.status_code < 300 and elapsed_time <= 0.5:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"


def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            
            domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

      
        for domain, stats in domain_stats.items():
            
            availability = int(100 * stats["up"] / stats["total"])
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)


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