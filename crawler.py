from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama, time

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

#initialize urls
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def crawl(url, max_urls=30):
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        return crawl(link, max_urls=max_urls)

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_links(url):
    urls = set()
    domain = urlparse(url).netloc
    session = HTMLSession()
    response = session.get(url)
    try:
        response.html.render()
    except:
        pass

    soup = BeautifulSoup(response.html.html, 'html.parser')
    for a_tag in soup.findAll('a'):
        href = a_tag.attrs.get('href')
        if href == "" or href is None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain not in href:
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

if __name__ == "__main__":
    start = time.process_time()

    import argparse
    parser = argparse.ArgumentParser(description="Crawling with Python3")
    parser.add_argument("url", help="The url to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max urls to crawl", default=20, type=int)
    
    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    crawl(url, max_urls=max_urls)

    # prints output on the Terminal
    print("[\n+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total Time Taken:", time.process_time() - start, "ms")

class Indexer:
    # storing pages in a file 
    internal_link = "internal_links.json" 
    with open(internal_link, "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    with open(f"external_links.json", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)