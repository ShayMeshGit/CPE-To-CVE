import requests
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

CPE_BASE_URL = "https://services.nvd.nist.gov/rest/json/cpes/2.0"
CVE_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

class NVDHandler:

    def __init__(self, console, results_per_page=2):
        self.console = console
        self.results_per_page = results_per_page

    """Fetch CPEs matching the keyword"""
    def fetch_CPEs_by_keyword(self, keyword, offset=None):
        params = {"keywordSearch": keyword, "resultsPerPage": self.results_per_page}
        if offset:
            params["startIndex"] = offset
        with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(f"[bold blue]Searching CPEs for '{keyword}'...", total=None)
            try:
                response = requests.get(url=CPE_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json().get('products', [])
                progress.update(task, description=f"[bold green]Request Complete!")
                return data
            except requests.RequestException as e:
                progress.update(task, description=f"[bold red]Error: {str(e)}")
                self.console.print(f"Error fetching CPEs: {e}")
                return []

    """Fetch CVEs for a specific CPE"""
    def fetch_CVEs_by_cpe_name(self, cpe_name):
        params = {"cpeName": cpe_name}
        with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]{task.description}"),
                TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(f"[bold blue]Fetching vulnerabilities for {cpe_name}...", total=None)
            try:
                response = requests.get(url=CVE_BASE_URL, params=params)
                response.raise_for_status()
                data = response.json().get('vulnerabilities', [])
                progress.update(task, description=f"[bold green]Request Complete!")
                return data
            except requests.RequestException as e:
                progress.update(task, description=f"[bold red]Error: {str(e)}")
                self.console.print(f"[red]Error fetching CVEs: {e}[/red]")
                return []