from rich.table import Table


CVSS_V31_KEY = 'cvssMetricV31'
CVSS_V30_KEY = 'cvssMetricV30'

class ConsoleDisplayHandler:
    def __init__(self, console):
        self.console = console

    def display_cpes(self, cpes):
        """Display CPEs in a table"""
        table = Table(title="\nFound CPEs")
        table.add_column("No.")
        table.add_column("CPE Name")

        for index, cpe in enumerate(cpes, 1):
            number = str(index)
            cpe_name = cpe['cpe']['titles'][0]['title']
            table.add_row(number, cpe_name)

        table.add_row()
        table.add_row('0', 'Next Page')
        self.console.print(table)

    def display_vulnerabilities(self, vulnerabilities, severity_filter=None):
        """Display CVEs in a table"""
        table = Table(title="\nVulnerabilities")
        table.add_column("CVE ID", style="red")
        table.add_column("Severity", style="yellow")
        table.add_column("Description", style="blue")

        for vuln in vulnerabilities:
            cve = vuln['cve']
            cve_id = cve['id']
            cve_description = cve['descriptions'][0]['value']
            (severity_score, severity) = self._get_vuln_severity(cve['metrics'])

            if severity_filter and severity != severity_filter:
                continue

            if not severity_score and not severity:
                continue

            table.add_row(cve_id, str(severity_score), cve_description)

        if table.row_count == 0:
            self.console.print("\n\nNo vulnerabilities found (In version 3.x), please try again or change the filter.")
            return

        self.console.print(table)

    def display_severity_filter_prompt(self):
        severity_filter = None
        answer = input('\nDo you wish to filter by severity? [y/N]: ').strip().lower()

        if answer == 'y' or answer == 'yes':
            self.console.print("\n\nSelect a severity filter:")
            self.console.print("1. Critical")
            self.console.print("2. High")
            self.console.print("3. Medium")
            self.console.print("4. Low")
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