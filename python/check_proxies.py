import aiohttp
import asyncio

# List of proxies to check
proxies = [
    "194.169.202.177:6582",
    "64.64.115.243:5878",
    "91.211.87.122:7112",
    "89.43.32.83:5911",
    "161.123.131.225:5830",
    "194.38.27.13:6574",
    "185.226.205.12:5544",
    "92.42.0.6:6496",
    "104.222.167.103:6505",
    "104.239.2.208:6511",
    "104.250.204.44:6135",
    "192.177.87.67:5913"
]

async def check_proxy(proxy):
    """Check if a proxy is working."""
    test_url = "http://ip-api.com/json/?fields=61439"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(test_url, proxy=f"http://{proxy}", timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"Proxy {proxy} is working. IP: {data.get('query')}")
                    return proxy
    except aiohttp.ClientProxyConnectionError:
        print(f"Proxy connection error for {proxy}")
    except aiohttp.ClientHttpProxyError:
        print(f"HTTP proxy error for {proxy}")
    except asyncio.TimeoutError:
        print(f"Timeout error for {proxy}")
    except Exception as e:
        print(f"Error checking proxy {proxy}: {e}")
    return None

async def main():
    """Main function to check all proxies."""
    tasks = [check_proxy(proxy) for proxy in proxies]
    working_proxies = await asyncio.gather(*tasks)
    working_proxies = [proxy for proxy in working_proxies if proxy]

    # Write working proxies to a new file
    with open("working_proxies.txt", "w") as file:
        for proxy in working_proxies:
            file.write(f"{proxy}\n")
    print(f"Working proxies saved to working_proxies.txt")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main()) 