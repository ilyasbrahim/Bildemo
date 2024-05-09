import tkinter as tk
from tkinter import messagebox, filedialog
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


def get_car_data(car_url, telefonnummer, checkmarks):
    response = requests.get(car_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        car_model_row_1 = soup.find_all('li', class_='row')[0]
        car_model_element_1 = car_model_row_1.find('div', class_='col-auto')
        car_model_1 = car_model_element_1.text.strip()

        car_model_row_2 = soup.find_all('li', class_='row')[1]
        car_model_element_2 = car_model_row_2.find('div', class_='col-auto')
        car_model_2 = car_model_element_2.text.strip()

        car_model = f"{car_model_1} {car_model_2}"

        year_row = soup.find_all('li', class_='row')[2]
        year_element = year_row.find('div', class_='col-auto')
        year = year_element.text.strip()

        status_row = soup.find_all('li', class_='row')[3]
        status_element = status_row.find('div', class_='col-auto')
        status = status_element.text.strip()

        mileage_row = soup.find_all('li', class_='row')[9]
        mileage_element = mileage_row.find('div', class_='col-auto')
        mileage = mileage_element.text.strip()

        mot_row = soup.find_all('li', class_='row')[10]
        mot_element = mot_row.find('div', class_='col-auto')
        mot_expiry_date = mot_element.text.strip()

        return {
            "Bilmodell": car_model,
            "Årsmodell": year,
            "Mätarställning": mileage,
            "Utgången Besiktning": mot_expiry_date,
            "Status": status,
            "Telefonnummer": telefonnummer,
            "Klar": checkmarks
        }
    return None


def scrape_cars(url, start_date, end_date, result_text, excel_name_entry):
    car_list = []

    excel_file_name = excel_name_entry.get()
    subdirectory = "Lista"  # Subdirectory name

    script_dir = os.path.dirname(os.path.realpath(__file__))

    current_page = 1
    while True:
        response = requests.get(f"{url}&page={current_page}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            car_elements = soup.find_all('a', class_='d-none d-md-inline-block font-weight-bold')

            for car_element in car_elements:
                car_url = car_element['href']
                mot_info = get_car_data(car_url, "", "") 
                if mot_info:
                    mot_expiry_date = mot_info["Utgången Besiktning"]
                    if start_date <= mot_expiry_date <= end_date:
                        car_list.append({
                            "URL": car_url,
                            "Bilmodell": mot_info["Bilmodell"],
                            "Årsmodell": mot_info["Årsmodell"],
                            "Mätarställning": mot_info["Mätarställning"],
                            "Utgången Besiktning": mot_expiry_date,
                            "Status": mot_info["Status"],
                            "Regnr": "", 
                            "Telefonnummer": "",
                            "Klar": ""
                        })

            next_button = soup.find('a', class_='pagination__next')
            if not next_button:
                break 

            current_page += 1  

        else:
            break  

    excel_file_path = os.path.join(subdirectory, f"{excel_file_name}.xlsx")

    df = pd.DataFrame(car_list, columns=["URL", "Bilmodell", "Årsmodell", "Mätarställning", "Utgången Besiktning", "Status", "Regnr", "Telefonnummer", "Klar"])

    df.to_excel(excel_file_path, index=False)

    return excel_file_path 


def run_scraper():
    try:
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        main_url = main_link_entry.get()

        excel_file_name = excel_name_entry.get()

        script_dir = os.path.dirname(os.path.realpath(__file__))
        excel_file_path = os.path.join(script_dir, f"{excel_file_name}.xlsx")

        result = scrape_cars(main_url, start_date, end_date, result_text, excel_name_entry)

        messagebox.showinfo("Scraping Complete", f"Scraping process is complete. Excel file saved at: {result}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# GUI setup
app = tk.Tk()
app.title("Car Scraper")
app.geometry("800x600") 
app.configure(bg="#FFFFFF")

main_link_label = tk.Label(app, text="Ange URL:", font=("Arial", 20), bg="#FFFFFF", fg="#000000", padx=10, pady=1)
main_link_label.pack(pady=1)

main_link_entry = tk.Entry(app, font=("Arial", 14), width=50) 
main_link_entry.pack(pady=10)

mot_date_label = tk.Label(app, text="Ange Senast Besiktning:", font=("Arial", 15), bg="#FFFFFF", fg="#000000",
                           padx=10, pady=1)
mot_date_label.pack(pady=1)

start_date_label = tk.Label(app, text="Start Datum (YYYY-MM-DD):", font=("Arial", 14), bg="#FFFFFF", fg="#000000",
                             padx=10, pady=1)
start_date_label.pack(pady=1)

start_date_entry = tk.Entry(app, font=("Arial", 14))
start_date_entry.pack(pady=10)

end_date_label = tk.Label(app, text="Slut Datum (YYYY-MM-DD):", font=("Arial", 14), bg="#FFFFFF", fg="#000000",
                           padx=10, pady=1)
end_date_label.pack(pady=1)

end_date_entry = tk.Entry(app, font=("Arial", 14))
end_date_entry.pack(pady=10)

excel_name_label = tk.Label(app, text="Excel File Name:", font=("Arial", 15), bg="#FFFFFF", fg="#000000",
                            padx=10, pady=1)
excel_name_label.pack(pady=1)

excel_name_entry = tk.Entry(app, font=("Arial", 14))
excel_name_entry.pack(pady=10)

scrape_button = tk.Button(app, text="Hitta bilar", command=run_scraper, font=("Arial", 20), fg="#000000",
                          bg="#064789", padx=10, pady=5)
scrape_button.pack(pady=10)

result_text = tk.Text(app, height=30, width=70, state=tk.DISABLED, wrap="word", font=("Arial", 20), fg="#000000",
                      bg="#999999", padx=10, pady=10)
result_text.pack(pady=10)

app.mainloop()
