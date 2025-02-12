from rich.console import Console
from rich import print
from CLIApp import CLIApp

def main():
    try:
        app = CLIApp(Console(color_system="standard"))
        app.run()
    except Exception as e:
        print('\n\n[bold red]Oops! Something went wrong, please try running the script again :([/bold red]\n\n')

if __name__ == "__main__":
    main()