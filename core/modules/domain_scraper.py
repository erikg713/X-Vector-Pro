import tldextract
import requests
from bs4 import BeautifulSoup

def extract_domains(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    links = soup.find_all('a', href=True)
    domains = set()
    for link in links:
        ext = tldextract.extract(link['href'])
        if ext.domain and ext.suffix:
            domains.add(f"{ext.domain}.{ext.suffix}")
    return domains

if __name__ == "__main__":
    url = input("Enter URL to extract domains: ")
    print(extract_domains(url))
