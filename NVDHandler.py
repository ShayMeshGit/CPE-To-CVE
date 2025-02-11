import requests

CPE_BASE_URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0"
CVE_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

class NVDHandler:

    def __init__(self, console, api_key, results_per_page=2):
        self.console = console
        self.results_per_page = results_per_page
        self.headers = {"apiKey": api_key}

    """Fetch CPEs matching the keyword"""
    def fetch_CPEs_by_keyword(self, keyword, offset=None):
        params = {"keywordSearch": keyword, "resultsPerPage": self.results_per_page}
        if offset:
            params["startIndex"] = offset
        try:
            response = requests.get(url=CPE_BASE_URL, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get('products')
        except requests.RequestException as e:
            self.console.print(f"Error fetching CPEs: {e}")
            return []

    """Fetch CVEs for a specific CPE"""
    def fetch_CVEs_by_cpe_name(self, cpe_name):
        params = {"cpeName": cpe_name}
        try:
            response = requests.get(url=CVE_BASE_URL, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json().get('vulnerabilities')
        except requests.RequestException as e:
            self.console.print(f"[red]Error fetching CVEs: {e}[/red]")
            return []