from rich.table import Table
from GithubHandler import get_github_rating


CVSS_V31_KEY = 'cvssMetricV31'
CVSS_V30_KEY = 'cvssMetricV30'

class ConsoleDisplayHandler:
    def __init__(self, console):
        self.console = console

    def display_cpes(self, cpes):
        """Display CPEs in a table"""
        table = Table(title="\nFound CPEs", style="green")
        table.add_column("No.", style='blue')
        table.add_column("CPE Name", style='blue')

        for index, cpe in enumerate(cpes, 1):
            number = str(index)
            cpe_name = cpe['cpe']['titles'][0]['title']
            table.add_row(number, cpe_name)

        table.add_row()
        table.add_row('0', 'Next Page')
        self.console.print(table)

    def display_vulnerabilities(self, vulnerabilities, severity_filter=None):
        """Display CVEs in a table"""
        table = Table(title="\nVulnerabilities", style="green")
        table.expand = True
        table.add_column("CVE ID", style="red")
        table.add_column("Severity", style="yellow")
        table.add_column("Description", style="blue")
        table.add_column("Github Resources", style="blue")

        for vuln in vulnerabilities:
            cve = vuln['cve']
            cve_id = cve['id']
            cve_description = cve['descriptions'][0]['value']
            (severity_score, severity) = self._get_vuln_severity(cve['metrics'])

            if severity_filter and severity != severity_filter:
                continue

            if not severity_score and not severity:
                continue

            sorted_github_urls = get_github_rating(cve['references'])
            github_table = self._get_github_table(sorted_github_urls)
            table.add_row(cve_id, str(severity_score), cve_description, github_table)

        if table.row_count == 0:
            self.console.print("\n\n[bold orange1]No vulnerabilities found (In version 3.x), please try again or change the filter.[/bold orange1]")
            return

        self.console.print(table)

    def display_severity_filter_prompt(self):
        severity_filter = None
        answer = input('\nDo you wish to filter by severity? [y/N]: ').strip().lower()

        if answer == 'y' or answer == 'yes':
            self.console.print("\n\nSelect a severity filter:")
            self.console.print("[bold red]1. Critical[/bold red]")
            self.console.print("[bold orange1]2. High[/bold orange1]")
            self.console.print("[bold cyan]3. Medium[/bold cyan]")
            self.console.print("[bold blue]4. Low[/bold blue]")
            severity_filter_choice = input('\nYour choice (1-4): ')
            if severity_filter_choice == '1':
                severity_filter = 'CRITICAL'
            elif severity_filter_choice == '2':
                severity_filter = 'HIGH'
            elif severity_filter_choice == '3':
                severity_filter = 'MEDIUM'
            elif severity_filter_choice == '4':
                severity_filter = 'LOW'

        return severity_filter

    def _get_github_table(self, github_data):
        table = Table()
        table.add_column("Exploit")
        table.add_column("Rating")

        for url, stars, rating in github_data:
            rating_display = "★" * rating
            formated_rating = f"[bold yellow]{rating_display} - {stars} stars[/bold yellow]"
            table.add_row(url, formated_rating)

        if table.row_count == 0:
            return "No github resources found"
        return table



    def _get_vuln_severity(self, metrics):
        """Get the severity of a vulnerability"""
        def get_data(version):
            cvss_data = version[0]['cvssData']
            base_score = cvss_data['baseScore']
            base_severity = cvss_data['baseSeverity']
            return base_score, base_severity

        version_31 = metrics.get(CVSS_V31_KEY, None)
        if version_31:
            return get_data(version_31)

        version_30 = metrics.get(CVSS_V30_KEY, None)
        if version_30:
            return get_data(version_30)

        return None, None