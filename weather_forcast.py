import tkinter as tk
from tkinter import messagebox
import requests
from io import BytesIO
from PIL import Image, ImageTk

# ------------------ Define the Function ------------------
def get_weather():
    global weather_icon

    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name!")
        return

    api_key = "489a0f5060b3c4a296923a4dc3cc3893"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            city_name = data["name"]
            country = data["sys"]["country"]
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"].capitalize()
            icon_code = data["weather"][0]["icon"]

            # Weather Icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_response = requests.get(icon_url)
            icon_data = Image.open(BytesIO(icon_response.content))
            icon_image = ImageTk.PhotoImage(icon_data)
            weather_icon.config(image=icon_image)
            weather_icon.image = icon_image

            # Show the result
            weather_label.config(
                text=f"{city_name}, {country}\n🌡 {temp}°C\n☁ {description}"
            )

        else:
            messagebox.showerror("Error", f"City not found: {city}")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")


# ------------------Delete the text when clean the search ------------------
def on_city_change(event):
    text = city_entry.get().strip()
    if not text:
        weather_label.config(text="")
        weather_icon.config(image="")
        weather_icon.image = None


# ------------------ GUI ------------------
root = tk.Tk()
root.title("Weather App 🌤")
root.geometry("400x500")
root.resizable(False, False)
root.configure(bg="#f1f5f9")

PRIMARY = "#2563eb"
SECONDARY = "#1e3a8a"
TEXT_COLOR = "#0f172a"
BG_COLOR = "#f1f5f9"

# ---------- Label ----------
title_label = tk.Label(root,
                       text="Weather Forecast",
                       font=("Segoe UI", 20, "bold"),
                       fg=PRIMARY,
                       bg=BG_COLOR)
title_label.pack(pady=20)

# ---------- Exit ----------
frame = tk.Frame(root, bg=BG_COLOR)
frame.pack(pady=10)

city_entry = tk.Entry(frame,
                      font=("Segoe UI", 14),
                      width=20,
                      justify="center",
                      relief="solid",
                      bd=1)
city_entry.grid(row=0, column=0, padx=10)

# Change the text
city_entry.bind("<KeyRelease>", on_city_change)

search_button = tk.Button(frame, text="Search", command=get_weather,
                          font=("Segoe UI", 12, "bold"), bg=PRIMARY, fg="white",
                          activebackground=SECONDARY, activeforeground="white",
                          relief="flat", cursor="hand2", padx=10, pady=5)
search_button.grid(row=0, column=1)

# ---------- Icon ----------
weather_icon = tk.Label(root, bg=BG_COLOR)
weather_icon.pack(pady=20)

# ---------- Result ----------
weather_label = tk.Label(root,
                         text="",
                         font=("Segoe UI", 16),
                         bg=BG_COLOR,
                         fg=TEXT_COLOR,
                         justify="center")
weather_label.pack(pady=20)

# ---------- Footer ----------
footer_label = tk.Label(root,
                        text="Developed by Majid 🌙",
                        font=("Segoe UI", 10, "italic"),
                        bg=BG_COLOR,
                        fg="#64748b")
footer_label.pack(side="bottom", pady=15)

root.mainloop()



