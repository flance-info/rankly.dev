import requests

def check_proxy(proxy_ip, proxy_port, protocol):
    """Check if a specific proxy is working."""
    proxy_url = f"{protocol.lower()}://{proxy_ip}:{proxy_port}"
    test_url = "https://wp-rankings.com/plugins/"  # Alternative test endpoint
    proxies = {"http": proxy_url, "https": proxy_url}

    try:
        print(f"Testing proxy: {proxy_url}")
        response = requests.get(test_url, proxies=proxies, timeout=30)  # Extended timeout
        if response.status_code == 200:
            print(f"Proxy is working: {proxy_url}")
            print(f"Returned IP: {response.json().get('ip')}")
        else:
            print(f"Proxy failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Proxy failed: {proxy_url} | Error: {e}")

# Proxy details
proxies = [
    {"ip": "45.202.78.210", "port": "3128", "protocol": "HTTP"},
    {"ip": "156.253.165.189", "port": "3128", "protocol": "HTTP"}
]

# Test each proxy
for proxy in proxies:
    check_proxy(proxy["ip"], proxy["port"], proxy["protocol"])
