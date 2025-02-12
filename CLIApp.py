from NVDHandler import NVDHandler
from ConsoleDisplayHandler import ConsoleDisplayHandler
RESULTS_PER_PAGE = 15

class CLIApp:
    def __init__(self, console, api_key=None):
        self.console = console
        self.nvd_service = NVDHandler(self.console, api_key, RESULTS_PER_PAGE)
        self.display_service = ConsoleDisplayHandler(self.console)

    def run(self):
        self.console.print("\nWelcome to CPE to CVE Lookup Tool")

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
                    self.console.print("\n\nNo CPEs were found. Please try a different keyword.")
                    break

                # Display CPEs
                self.display_service.display_cpes(found_cpes)

                # Select CPE
                try:
                    cpe_index = int(input("\nSelect a CPE number (0 for next page): ").strip()) - 1

                    if cpe_index == -1:
                        offset += RESULTS_PER_PAGE
                        continue

                    selected_cpe_name = found_cpes[cpe_index]['cpe']['cpeName']

                    # Display Severity Filter Choices
                    severity_filter = self.display_service.display_severity_filter_prompt()

                    # Fetch and display CVEs
                    vulnerabilities = self.nvd_service.fetch_CVEs_by_cpe_name(selected_cpe_name)

                    if not vulnerabilities:
                        self.console.print("\n\nNo vulnerabilities found for the selected CPE. Please try again.")
                    else:
                        self.display_service.display_vulnerabilities(vulnerabilities, severity_filter)

                    self.console.print("\n\nThank you for using the tool! (:")
                    answer = input("\nDo you want to continue using the tool? [y/N]: ").strip().lower()
                    if answer == 'n' or answer == 'no':
                        continue_program = False
                    break
                except (ValueError, IndexError):
                    self.console.print("\n\nInvalid selection. Please try again.")
                    continue
        self.console.print("\nGoodbye!")