import requests
import random
from itertools import cycle

class ProxyManager:
    def __init__(self, proxy_sources=None):
        """
        Initializes the ProxyManager with optional proxy sources.
        :param proxy_sources: List of URLs to scrape proxies from.
        """
        self.proxy_sources = proxy_sources if proxy_sources else []
        self.proxy_list = []
        self.valid_proxies = []

    def scrape_proxies(self):
        """
        Scrapes proxies from the provided proxy sources.
        """
        print("Scraping proxies...")
        for source in self.proxy_sources:
            try:
                response = requests.get(source, timeout=10)
                response.raise_for_status()
                scraped_proxies = response.text.strip().split('\n')
                self.proxy_list.extend(scraped_proxies)
                print(f"Scraped {len(scraped_proxies)} proxies from {source}")
            except Exception as e:
                print(f"Failed to scrape proxies from {source}: {e}")

    def validate_proxies(self, test_url="https://httpbin.org/ip", timeout=5):
        """
        Validates the scraped proxies.
        :param test_url: The URL used to test proxy validity.
        :param timeout: Timeout for proxy requests.
        """
        print("Validating proxies...")
        self.valid_proxies = []
        for proxy in self.proxy_list:
            try:
                proxies = {"http": proxy, "https": proxy}
                response = requests.get(test_url, proxies=proxies, timeout=timeout)
                if response.status_code == 200:
                    self.valid_proxies.append(proxy)
                    print(f"Valid proxy: {proxy}")
            except Exception:
                print(f"Invalid proxy: {proxy}")

    def get_random_proxy(self):
        """
        Returns a random valid proxy.
        :return: A random proxy from the valid proxies list or None if no valid proxies exist.
        """
        if not self.valid_proxies:
            print("No valid proxies available.")
            return None
        return random.choice(self.valid_proxies)

    def get_rotating_proxy(self):
        """
        Returns a generator that cycles through the valid proxies.
        :return: A generator object cycling through valid proxies.
        """
        if not self.valid_proxies:
            print("No valid proxies available.")
            return None
        return cycle(self.valid_proxies)


if __name__ == "__main__":
    # Example usage
    proxy_sources = [
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://www.proxy-list.download/api/v1/get?type=http"
    ]
    proxy_manager = ProxyManager(proxy_sources)
    proxy_manager.scrape_proxies()
    proxy_manager.validate_proxies()

    # Get a random proxy
    random_proxy = proxy_manager.get_random_proxy()
    print(f"Random Proxy: {random_proxy}")

    # Use rotating proxies
    rotating_proxy = proxy_manager.get_rotating_proxy()
    if rotating_proxy:
        for _ in range(5):
            print(f"Rotating Proxy: {next(rotating_proxy)}")
