import requests
from bs4 import BeautifulSoup

GITHUB_BASE_URL = 'https://github.com/'

def extract_repo_url(github_url):
    try:
        github_base_url = GITHUB_BASE_URL
        url_data_arr = github_url.split(github_base_url)
        path_arr = url_data_arr[1].split('/')
        github_user = path_arr[0]
        repo = path_arr[1]
        return f"{GITHUB_BASE_URL}{github_user}/{repo}"
    except Exception:
        return None


def get_github_exploits_urls(references):
    github_exploits_urls = []

    for reference in references:
        if reference['url'].startswith(GITHUB_BASE_URL) and ('Exploit' in reference.get('tags',[])):
            repo_url = extract_repo_url(reference['url'])
            if not repo_url:
                continue
            github_exploits_urls.append(repo_url)

    return set(github_exploits_urls)

def fetch_github_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def extract_github_rating(html_content):
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    stars_tag = soup.find('a', href=lambda href: href and 'stargazers' in href)
    forks_tag = soup.find('a', href=lambda href: href and 'forks' in href)
    watchers_tag = soup.find('a', href=lambda href: href and 'watchers' in href)

    def get_rating(count):
        if 'k' in count:
            return 3
        int_count = int(count)
        if int_count < 100:
            return 1
        elif int_count < 1000:
            return 2

    stars_count = 0
    star_rating = 0
    forks_rating = 0
    watchers_rating = 0

    if stars_tag:
        stars_count = stars_tag.find('span', class_='text-bold').text.strip()
        star_rating = get_rating(stars_count)
    if forks_tag:
        forks_count = forks_tag.find('span', class_='text-bold').text.strip()
        forks_rating = get_rating(forks_count)
    if watchers_tag:
        watchers_count = watchers_tag.find('strong').text.strip()
        watchers_rating = get_rating(watchers_count)

    # Average of the 3 ratings
    final_rating = (star_rating + forks_rating + watchers_rating) / 3

    return stars_count, round(final_rating)


def get_github_rating(references):
    github_exploits_urls = get_github_exploits_urls(references)
    rated_urls = []

    for url in github_exploits_urls:
        html_text = fetch_github_page(url)
        if html_text:
            (github_stars, stars) = extract_github_rating(html_text)
            rated_urls.append((url,github_stars,stars))

    # Sort URLs based on rating in descending order
    rated_urls.sort(key=lambda x: x[2], reverse=True)

    return rated_urls
