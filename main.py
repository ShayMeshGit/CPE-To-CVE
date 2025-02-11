from rich.console import Console
from CLIApp import CLIApp
from dotenv import load_dotenv
import os

load_dotenv()

NVD_API_KEY=os.getenv('NVD_API_KEY')

def main():
    try:
        app = CLIApp(Console(), NVD_API_KEY)
        app.run()
    except Exception as e:
        print('Oops! Something went wrong, please try running the script again ):')

if __name__ == "__main__":
    main()