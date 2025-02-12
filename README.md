# How to Run the Program

A Python-based security tool that helps users discover vulnerabilities in software and hardware by searching the National Vulnerability Database (NVD) using CPE identifiers and provides detailed CVE information along with related GitHub exploit repositories.

## Prerequisites

1. **Python 3.8 or Higher**  
   Ensure Python is installed. Download it from [python.org](https://www.python.org/).
2. **Install Dependencies**  
   Open your terminal and navigate to the directory containing the program files:  
   ```bash
   cd path/to/project
   ```
   Then, install the required Python packages by running:  
   ```bash
   pip install -r requirements.txt
   ```

## Steps to Run

1. **Navigate to the Project Directory**  
   Open your terminal and navigate to the directory containing the program files:  
   ```bash
   cd path/to/project
   ```

2. **Run the Program**  
   Execute the program using Python:  
   ```bash
   python main.py
   ```

## Notes

- If you encounter errors, verify that all dependencies are correctly installed.
- Due to API-related issues, sometimes the request fails and needs to be queried again.
