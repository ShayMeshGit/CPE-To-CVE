


class GitHubHandler:
    def __init__(self, token):
        self.token = token

    @staticmethod
    def get_github_exploits_urls(references):
        github_exploits_urls = []
        for reference in references:
            if reference['url'].startswith("https://github.com/") and 'Exploit' in reference['tags']:
                github_exploits_urls.append(reference['url'])
        return set(github_exploits_urls)