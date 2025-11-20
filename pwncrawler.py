#!/usr/bin/env python3
"""
PwnCrawler - Web Crawler
Author: Emilio Pancubit
Description:
    A lightweight web crawler that collects URLs from a target website.
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import sys
import json

class PwnCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.to_visit = [base_url]

    def is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        except:
            return False

    def crawl(self):
        print(f"[+] Starting PwnCrawler on: {self.base_url}\n")

        while self.to_visit:
            url = self.to_visit.pop(0)
            if url in self.visited:
                continue

            self.visited.add(url)
            print(f"[*] Crawling: {url}")

            try:
                response = requests.get(url, timeout=10)
            except requests.RequestException as e:
                print(f"[!] Error accessing {url}: {e}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                new_url = urljoin(url, link.get("href"))

                if self.is_valid_url(new_url) and new_url.startswith(self.base_url):
                    if new_url not in self.visited and new_url not in self.to_visit:
                        print(f"    [+] Found: {new_url}")
                        self.to_visit.append(new_url)

        print("\n[+] Crawling complete!")
        print(f"[+] Total URLs found: {len(self.visited)}")

        domain = urlparse(self.base_url).netloc
        output_file = f"{domain}_pwncrawler.json"
        with open(output_file, "w") as f:
            json.dump(list(self.visited), f, indent=4)
        print(f"[+] Output saved to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pwncrawler.py <URL>")
        sys.exit(1)

    target_url = sys.argv[1]

    crawler = PwnCrawler(target_url)
    crawler.crawl()