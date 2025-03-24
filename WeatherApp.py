import requests
import tkinter as tk
from tkinter import messagebox, StringVar


api_key = "-------"

def fetch_weather():
    location = location_var.get().strip()
    if not location:
        messagebox.showerror("Error", "Please enter a location")
        return

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
        )
        data = response.json()

        if data.get('cod') != 200:
            messagebox.showerror("Error", f"Invalid location: {location}")
            return


        description = data['weather'][0]['description']
        temperature = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        high = round(data['main']['temp_max'])
        low = round(data['main']['temp_min'])

        result = (
            f"Weather in {location.capitalize()}:\n\n"
            f"Temperature: {temperature}°C\n"
            f"Description: {description.capitalize()}\n"
            f"Feels Like: {feels_like}°C\n"
            f"High: {high}°C, Low: {low}°C"
        )
        weather_output.set(result)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def get_suggestions(event):
    query = location_var.get().strip()
    if not query:
        suggestions_list.delete(0, tk.END)
        return
    try:

        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}"
        )
        if response.status_code == 200:
            data = response.json()
            suggestions = [f"{item['name']}, {item['country']}" for item in data]


            suggestions_list.delete(0, tk.END)
            for suggestion in suggestions:
                suggestions_list.insert(tk.END, suggestion)
    except Exception as e:
        messagebox.showerror("Error", f"Unable to fetch suggestions: {e}")


def select_suggestion(event):
    selected = suggestions_list.get(suggestions_list.curselection())
    location_var.set(selected)
    suggestions_list.delete(0, tk.END)


root = tk.Tk()
root.title("Weather App")


location_var = StringVar()
weather_output = StringVar()


input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Enter Location:").grid(row=0, column=0, padx=5, pady=5)
location_entry = tk.Entry(input_frame, textvariable=location_var, width=30)
location_entry.grid(row=0, column=1, padx=5, pady=5)
location_entry.bind("<KeyRelease>", get_suggestions)

fetch_button = tk.Button(input_frame, text="Get Weather", command=fetch_weather)
fetch_button.grid(row=0, column=2, padx=5, pady=5)


suggestions_frame = tk.Frame(root)
suggestions_frame.pack(pady=5)

suggestions_list = tk.Listbox(suggestions_frame, width=40, height=5)
suggestions_list.pack()
suggestions_list.bind("<<ListboxSelect>>", select_suggestion)


output_frame = tk.Frame(root)
output_frame.pack(pady=10)

weather_label = tk.Label(
    output_frame, textvariable=weather_output, justify="left", font=("Helvetica", 12), wraplength=400
)
weather_label.pack()

root.mainloop()