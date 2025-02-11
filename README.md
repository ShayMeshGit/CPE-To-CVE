# How to Run the Program

## Prerequisites

1. **Python 3.8 or Higher**  
   Ensure Python is installed. Download it from [python.org](https://www.python.org/).

2. **Install Dependencies**  
   Install the required Python packages by running:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up API Key**  
   - Create a `.env` file in the project's root directory.  
   - Add your **NVD API Key** in the following format:  
     ```
     NVD_API_KEY=your_nvd_api_key
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

- Ensure that a valid **NVD API Key** is present in the `.env` file; the program won't run without it.
- If you encounter errors, verify that all dependencies are correctly installed and that the `.env` file is properly configured.
