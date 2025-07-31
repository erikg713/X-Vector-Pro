import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

COMMON_SUBDOMAINS = [
    "www", "blog", "shop", "dev", "test", "api", "staging", "mail", "ftp", "admin"
]

class SubdomainEnum:
    def __init__(self, domain, threads=10, timeout=3):
        self.domain = domain
        self.threads = threads
        self.timeout = timeout
        self.found_subdomains = []

    def check_subdomain(self, subdomain):
        url = f"http://{subdomain}.{self.domain}"
        try:
            r = requests.get(url, timeout=self.timeout)
            if r.status_code < 400:
                return url
        except requests.RequestException:
            return None

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_subdomain, sd): sd for sd in COMMON_SUBDOMAINS}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.found_subdomains.append(result)
        return self.found_subdomains
