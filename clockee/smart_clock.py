import tkinter as tk
from tkinter import ttk, messagebox
import time
import datetime
import calendar
import platform


BG = "#0d0d0d"
FG = "#ffffff"
ACCENT = "#1e1e1e"
BUTTON_BG = "#2a2a2a"
BUTTON_FG = "#ffffff"
TAB_BG = "#111111"
TAB_ACTIVE = "#222222"
LIST_BG = "#1a1a1a"
LIST_FG = "#ffffff"
TODAY_COLOR = "#4444aa"   


is_24_hour_format = True
clock_after_id = None

stopwatch_running = False
stopwatch_start_time = 0.0
stopwatch_elapsed = 0.0
stopwatch_after_id = None


def center_window(win, w, h):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


def update_clock():
    global clock_after_id

    if clock_after_id is not None:
        try:
            clock_label.after_cancel(clock_after_id)
        except:
            pass

    now = datetime.datetime.now()
    time_text = now.strftime("%H:%M:%S") if is_24_hour_format else now.strftime("%I:%M:%S %p")
    date_text = now.strftime("%A, %B %d, %Y")

    clock_label.config(text=time_text)
    date_label.config(text=date_text)

    clock_after_id = clock_label.after(1000, update_clock)

def toggle_format():
    global is_24_hour_format
    is_24_hour_format = not is_24_hour_format
    update_clock()


def format_time(ms):
    hours = int(ms // 3600)
    minutes = int((ms % 3600) // 60)
    seconds = int(ms % 60)
    centis = int((ms - int(ms)) * 100)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{centis:02d}"
    return f"{minutes:02d}:{seconds:02d}.{centis:02d}"

def sw_update():
    global stopwatch_after_id, stopwatch_elapsed
    if stopwatch_running:
        now = time.perf_counter()
        elapsed = stopwatch_elapsed + (now - stopwatch_start_time)
        sw_label.config(text=format_time(elapsed))
        stopwatch_after_id = sw_label.after(50, sw_update)

def sw_start():
    global stopwatch_running, stopwatch_start_time
    if not stopwatch_running:
        stopwatch_running = True
        stopwatch_start_time = time.perf_counter()
        sw_update()

def sw_stop():
    global stopwatch_running, stopwatch_elapsed, stopwatch_start_time
    if stopwatch_running:
        now = time.perf_counter()
        stopwatch_elapsed += (now - stopwatch_start_time)
        stopwatch_running = False
        sw_label.config(text=format_time(stopwatch_elapsed))

def sw_reset():
    global stopwatch_elapsed, stopwatch_running
    stopwatch_running = False
    stopwatch_elapsed = 0.0
    sw_label.config(text="00:00.00")
    lap_list.delete(0, tk.END)

def sw_lap():
    lap_list.insert(0, sw_label.cget("text"))


cal_year = datetime.datetime.now().year
cal_month = datetime.datetime.now().month

def draw_calendar():
    today = datetime.datetime.now()

    for w in cal_frame.winfo_children():
        w.destroy()

    tk.Label(cal_frame, text=f"{calendar.month_name[cal_month]} {cal_year}",
             fg=FG, bg=BG, font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=7, pady=5)

    days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i, d in enumerate(days):
        tk.Label(cal_frame, text=d, fg=FG, bg=BG).grid(row=1, column=i)

    month = calendar.monthcalendar(cal_year, cal_month)

    for r, week in enumerate(month):
        for c, day in enumerate(week):
            txt = "" if day == 0 else str(day)

            # Highlight today's date
            if (day == today.day and cal_month == today.month and cal_year == today.year):
                bg_color = TODAY_COLOR
            else:
                bg_color = BUTTON_BG

            b = tk.Button(cal_frame, text=txt, width=4, height=1,
                          bg=bg_color, fg=BUTTON_FG,
                          command=lambda d=day: on_day_click(d))
            b.grid(row=r+2, column=c, padx=2, pady=2)

def on_day_click(day):
    if day != 0:
        messagebox.showinfo("Date Selected", f"{cal_year}-{cal_month:02d}-{day:02d}")

def prev_month():
    global cal_month, cal_year
    cal_month -= 1
    if cal_month < 1:
        cal_month = 12
        cal_year -= 1
    draw_calendar()

def next_month():
    global cal_month, cal_year
    cal_month += 1
    if cal_month > 12:
        cal_month = 1
        cal_year += 1
    draw_calendar()


window = tk.Tk()
window.title("Dark Time Suite")
window.configure(bg=BG)
center_window(window, 700, 450)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab", background=TAB_BG, foreground=FG, padding=8)
style.map("TNotebook.Tab", background=[("selected", TAB_ACTIVE)])

notebook = ttk.Notebook(window)
notebook.pack(fill="both", expand=True)


tab_clock = tk.Frame(notebook, bg=BG)
notebook.add(tab_clock, text="Clock")

clock_label = tk.Label(tab_clock, font=("Courier", 44, "bold"), fg=FG, bg=BG)
clock_label.pack(pady=10)

date_label = tk.Label(tab_clock, font=("Arial", 16), fg=FG, bg=BG)
date_label.pack()

toggle_btn = tk.Button(tab_clock, text="Toggle 12 / 24", bg=BUTTON_BG, fg=BUTTON_FG,
                       command=toggle_format)
toggle_btn.pack(pady=10)

# STOPWATCH TAB 
tab_sw = tk.Frame(notebook, bg=BG)
notebook.add(tab_sw, text="Stopwatch")

sw_label = tk.Label(tab_sw, text="00:00.00", font=("Courier", 40, "bold"), fg=FG, bg=BG)
sw_label.pack(pady=10)

btns = tk.Frame(tab_sw, bg=BG)
btns.pack()

tk.Button(btns, text="Start", bg=BUTTON_BG, fg=BUTTON_FG, width=8, command=sw_start).grid(row=0, column=0, padx=5)
tk.Button(btns, text="Stop", bg=BUTTON_BG, fg=BUTTON_FG, width=8, command=sw_stop).grid(row=0, column=1, padx=5)
tk.Button(btns, text="Lap", bg=BUTTON_BG, fg=BUTTON_FG, width=8, command=sw_lap).grid(row=0, column=2, padx=5)
tk.Button(btns, text="Reset", bg=BUTTON_BG, fg=BUTTON_FG, width=8, command=sw_reset).grid(row=0, column=3, padx=5)

lap_list = tk.Listbox(tab_sw, height=8, bg=LIST_BG, fg=LIST_FG)
lap_list.pack(fill="x", padx=20, pady=10)


tab_cal = tk.Frame(notebook, bg=BG)
notebook.add(tab_cal, text="Calendar")

controls = tk.Frame(tab_cal, bg=BG)
controls.pack()

tk.Button(controls, text="<< Prev", bg=BUTTON_BG, fg=BUTTON_FG,
          command=prev_month).pack(side="left", padx=10)
tk.Button(controls, text="Next >>", bg=BUTTON_BG, fg=BUTTON_FG,
          command=next_month).pack(side="right", padx=10)

cal_frame = tk.Frame(tab_cal, bg=BG)
cal_frame.pack(pady=10)

draw_calendar()


update_clock()

window.mainloop()
