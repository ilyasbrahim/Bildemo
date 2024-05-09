# Bildemo: Web Scraper for Car Data

**Description:**  
Bildemo is a Python-based web scraper designed specifically for car dealerships and businesses. It efficiently gathers detailed car data from [biluppgifter.se](https://biluppgifter.se) based on user input, allowing dealerships to cold call or directly purchase vehicles. The program compiles comprehensive details into an Excel file, streamlining the process of identifying and evaluating cars for purchase.

## Features

- **Customizable Input:** Accepts user input for filtering cars based on specific criteria.
- **Data Extraction:** Utilizes `BeautifulSoup` for parsing website content to extract relevant car information.
- **Data Export:** Exports car data to an Excel file using `pandas` and `openpyxl`, providing comprehensive details:
  - Car model
  - Year
  - Mileage
  - M.O.T date
  - Status (if the car is in traffic)
  - Link to additional information (including registration number/license plate)
- **User-Friendly Interface:** Features a simple interface using `tkinter` for user interaction.

## Tech Stack

- **Languages/Frameworks:** Python, BeautifulSoup, pandas, tkinter
- **Tools/Libraries:** requests, openpyxl

## Installation and Usage


Ensure you have Python 3.x installed along with pip (Python's package manager).

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ilyasbrahim/Bildemo.git
   cd Bildemo

2. **Create a Virtual Environment (Optional but Recommended):**
   
    ```bash
    python3 -m venv venv

3. ***Install Dependencies:Install the required dependencies via the requirements.txt file:***
 
     ```bash
    pip install -r requirements.txt

4. ***Run the Application:***
   
   ```bash
   python Bildemo.py
