from NVDHandler import NVDHandler
from ConsoleDisplayHandler import ConsoleDisplayHandler
RESULTS_PER_PAGE = 15

class CLIApp:
    def __init__(self, console):
        self.console = console
        self.nvd_service = NVDHandler(self.console, RESULTS_PER_PAGE)
        self.display_service = ConsoleDisplayHandler(self.console)

    def run(self):
        self.console.print("\n[bold magenta]Welcome to CPE to CVE Lookup Tool[/bold magenta]")

        continue_program = True
        while continue_program:
            keyword = input("\nEnter a CPE keyword: ")
            if not keyword:
                self.console.print("Keyword cannot be empty. Please try again.")
                continue

            offset = 0
            while True:
                found_cpes = self.nvd_service.fetch_CPEs_by_keyword(keyword, offset)

                if not found_cpes or len(found_cpes) == 0:
                    self.console.print("\n\n[orange1]No CPEs were found. Please try again or with a different keyword.[/orange1]")
                    break

                # Display CPEs
                self.display_service.display_cpes(found_cpes)

                # Select CPE
                try:
                    cpe_index = int(input("\nSelect a CPE number (0 for next page -1 to go back): ").strip()) - 1

                    if cpe_index == -1:
                        if len(found_cpes) == RESULTS_PER_PAGE:
                            offset += RESULTS_PER_PAGE
                        continue
                    if cpe_index == -2:
                        offset -= RESULTS_PER_PAGE
                        if offset < 1:
                            offset = 0
                        continue

                    selected_cpe_name = found_cpes[cpe_index]['cpe']['cpeName']

                    # Display Severity Filter Choices
                    severity_filter = self.display_service.display_severity_filter_prompt()

                    # Fetch and display CVEs
                    vulnerabilities = self.nvd_service.fetch_CVEs_by_cpe_name(selected_cpe_name)

                    if not vulnerabilities:
                        self.console.print("\n\n[orange]No vulnerabilities found for the selected CPE. Please try again.[/orange]")
                    else:
                        self.display_service.display_vulnerabilities(vulnerabilities, severity_filter)

                    answer = input("\nDo you want to continue using the tool? [y/N]: ").strip().lower()
                    if answer == 'n' or answer == 'no':
                        continue_program = False
                    break
                except (ValueError, IndexError):
                    self.console.print("\n\n[bold orange1]Invalid selection. Please try again.[/bold orange1]")
                    continue
        self.console.print("\n\n[bold magenta]Thank you for using the tool! (:[/bold magenta]")
        self.console.print("\n[bold magenta]Goodbye![/bold magenta]")