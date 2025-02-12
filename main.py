from rich.console import Console
from CLIApp import CLIApp

def main():
    try:
        app = CLIApp(Console())
        app.run()
    except Exception as e:
        print('Oops! Something went wrong, please try running the script again ):')

if __name__ == "__main__":
    main()