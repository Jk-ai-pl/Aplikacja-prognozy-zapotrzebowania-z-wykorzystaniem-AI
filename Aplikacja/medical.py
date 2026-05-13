from tkinter import Toplevel, Label, Button, messagebox, HORIZONTAL, Scale
from tkcalendar import Calendar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter

class Medical:
    def __init__(self, master):
        self.master = master
        self.window = Toplevel(master)
        self.window.title("Zasoby medyczne")
        self.window.geometry("400x500")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.forecast_window_open = False

        self.start_label = Label(self.window, text="Data początkowa: nie wybrano", font=("Arial", 12))
        self.start_label.pack(pady=5)
        self.end_label = Label(self.window, text="Data końcowa: nie wybrano", font=("Arial", 12))
        self.end_label.pack(pady=5)

        Button(self.window, text="Wprowadź datę początkową", command=lambda: self.open_calendar("start")).pack(pady=5)
        Button(self.window, text="Wprowadź datę końcową", command=lambda: self.open_calendar("end")).pack(pady=5)
        Button(self.window, text="Generuj prognozę", command=self.generate_forecast).pack(pady=10)
        Button(self.window, text="Powrót", command=self.on_close).pack(pady=5)

        self.date_type = None

    def open_calendar(self, date_type):
        self.date_type = date_type
        self.cal_window = Toplevel(self.window)
        self.cal_window.title("Wybierz datę")
        self.cal = Calendar(self.cal_window, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)
        Button(self.cal_window, text="Zatwierdź", command=self.get_date).pack(pady=5)

    def get_date(self):
        selected_date = self.cal.get_date()
        if self.date_type == "start":
            self.start_label.config(text=f"Data początkowa: {selected_date}")
        else:
            self.end_label.config(text=f"Data końcowa: {selected_date}")
        self.cal_window.destroy()

    def generate_forecast(self):
        if self.forecast_window_open:
            messagebox.showwarning("Uwaga", "Okno z prognozą już istnieje. Zamknij je przed wygenerowaniem nowej.")
            return

        start_text = self.start_label.cget("text").replace("Data początkowa: ", "")
        end_text = self.end_label.cget("text").replace("Data końcowa: ", "")
        if start_text == "nie wybrano" or end_text == "nie wybrano":
            messagebox.showerror("Błąd", "Wybierz obie daty!")
            return

        try:
            dates = pd.date_range(start=start_text, end=end_text, freq='M')
        except:
            messagebox.showerror("Błąd", "Błędny zakres dat!")
            return

        demand = np.random.randint(50, 200, size=len(dates))
        unit = "tyś. szt."

        self._create_forecast_window(dates, demand, "Prognoza zapotrzebowania na zasoby medyczne", f"Medyczne ({unit})", unit)

    def _create_forecast_window(self, dates, demand, title, label, unit):
        forecast_win = Toplevel(self.window)
        forecast_win.title(title)
        forecast_win.geometry("1000x600")

        fig, ax = plt.subplots(figsize=(len(dates)/2, 5))
        line, = ax.plot(dates, demand, marker='o', label=label)
        ax.set_xlabel("Data")
        ax.set_ylabel(f"Ilość zasobów ({unit})")
        ax.set_title(title)
        ax.grid(True)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))

        annot = ax.annotate("", xy=(0,0), xytext=(15,15), textcoords="offset points",
                            bbox=dict(boxstyle="round", fc="yellow", alpha=0.7),
                            arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(ind):
            x, y = line.get_data()
            date = pd.Timestamp(x[ind["ind"][0]])
            annot.xy = (date, y[ind["ind"][0]])
            annot.set_text(f"{date.strftime('%Y-%m-%d')}\n{y[ind['ind'][0]]} {unit}")
            annot.get_bbox_patch().set_alpha(0.7)

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == ax:
                cont, ind = line.contains(event)
                if cont:
                    update_annot(ind)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        annot.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)

        canvas = FigureCanvasTkAgg(fig, master=forecast_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        def update_xlim(val):
            max_points = 12
            start = int(val)
            ax.set_xlim(dates[start], dates[min(start+max_points, len(dates)-1)])
            canvas.draw_idle()

        slider = Scale(forecast_win, from_=0, to=max(0, len(dates)-12), orient=HORIZONTAL, command=update_xlim, showvalue=0)
        slider.pack(fill="x")
        update_xlim(0)

        self.forecast_window_open = True

        def on_close_forecast():
            self.forecast_window_open = False
            forecast_win.destroy()

        forecast_win.protocol("WM_DELETE_WINDOW", on_close_forecast)

    def on_close(self):
        self.master.deiconify()
        self.window.destroy()
