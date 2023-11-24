import random
import string
import sys
from concurrent.futures import ThreadPoolExecutor
from socks5.server import Socks5Server

def generate_proxy_config(port, require_auth=False):
    """
    Generates a proxy configuration for a given port with optional authentication.

    :param port: Port number for the proxy server.
    :param require_auth: Boolean indicating if authentication is required.
    :return: Dictionary containing the proxy configuration.
    """
    config = {
        "host": "0.0.0.0",  # Binding to 0.0.0.0 to accept connections from any IP
        "port": port
    }

    if require_auth:
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        config.update({"username": username, "password": password})

    return config


def run_socks5_proxy(config):
    """
    Runs a SOCKS5 proxy server using the provided configuration.

    :param config: Dictionary containing the proxy configuration.
    """
    server = Socks5Server(
        host=config["host"],
        port=config["port"],
        username=config.get("username"),
        password=config.get("password")
    )

    with open("proxy.txt", "a") as f:
        # write host, port, username, password to file
        f.write(f"{config['host']}:{config['port']}:{config.get('username')}:{config.get('password')}\n")

    server.serve_forever()


def run_proxies_in_range(start_port, end_port, require_auth=False, max_threads=8):
    """
    Sets up SOCKS5 proxies on a range of ports using multithreading.

    :param start_port: The starting port number.
    :param end_port: The ending port number.
    :param require_auth: Boolean indicating if authentication is required.
    :param max_threads: Maximum number of threads to use.
    """
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for port in range(start_port, end_port + 1):
            config = generate_proxy_config(port, require_auth=require_auth)
            executor.submit(run_socks5_proxy, config)


# Example usage: Set up proxies on ports 8000 to 8010
run_proxies_in_range(7000, 7020, require_auth=True)
