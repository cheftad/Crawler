
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import mimetypes

visited_urls = set()

def get_image_urls(url, content, content_type):
    if 'html' in content_type:
        soup = BeautifulSoup(content, 'html.parser')
    elif 'xml' in content_type or 'xhtml' in content_type:
        soup = BeautifulSoup(content, 'lxml')
    else:
        return []

    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]
    img_urls = [urljoin(url, img_url) for img_url in img_urls]

    return img_urls

def crawl(url, domain):
    if url in visited_urls:
        return []

    visited_urls.add(url)
    print(f'Crawling: {url}')

    response = requests.get(url)
    content_type = response.headers.get('Content-Type', '').lower()

    if 'html' not in content_type and 'xml' not in content_type and 'xhtml' not in content_type:
        return []

    image_urls = get_image_urls(url, response.content, content_type)

    if 'html' in content_type:
        soup = BeautifulSoup(response.content, 'html.parser')
    elif 'xml' in content_type or 'xhtml' in content_type:
        soup = BeautifulSoup(response.content, 'lxml')
    else:
        return image_urls

    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        full_url = urljoin(url, href)
        if urlparse(full_url).netloc == domain and full_url not in visited_urls:
            image_urls.extend(crawl(full_url, domain))
            time.sleep(1)

    return image_urls

if __name__ == "__main__":
    start_url = 'https://trymima.com'  # Replace with the website you want to crawl
    domain = urlparse(start_url).netloc
    all_image_urls = crawl(start_url, domain)
    
    all_image_urls = list(set(all_image_urls))
    print(f'{len(all_image_urls)} images found:')
    for url in all_image_urls:
        print(url)

