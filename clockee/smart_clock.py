import tkinter as tk
import time

# Format toggle flag
is_24_hour_format = True

def update_clock():
    if is_24_hour_format:
        current_time = time.strftime("%H:%M:%S")
    else:
        current_time = time.strftime("%I:%M:%S %p")

    current_date = time.strftime("%A, %B %d, %Y")

    clock_label.config(text=current_time)
    date_label.config(text=current_date)
    window.after(1000, update_clock)

def toggle_format():
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format
    update_clock()  # Immediately refresh after toggle

# Main window
window = tk.Tk()
window.title("Digital Clock")
window.geometry("400x200")
window.configure(bg="black")
window.resizable(False, False)
window.attributes("-topmost", True)  # Always on top of other windows

# Clock label
clock_label = tk.Label(window, text="", font=("Courier", 40, "bold"), fg="white", bg="black")
clock_label.pack(pady=10)

# Date label
date_label = tk.Label(window, text="", font=("Arial", 14), fg="white", bg="black")
date_label.pack()

# Toggle format button
toggle_btn = tk.Button(window, text="Toggle 12/24 Hour", command=toggle_format)
toggle_btn.pack(pady=10)

# Start clock
update_clock()
window.mainloop()
