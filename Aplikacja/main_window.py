from tkinter import Button, Label
from construction import Construction
from medical import Medical
from energy import Energy
from education import Education
from food import Food

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Wybór zasobów")
        self.master.geometry("400x500")

        Label(master, text="Narzędzie przewidywania zapotrzebowania na zasoby",
              font=("Arial", 14), wraplength=350, justify="center").pack(pady=20)
        Label(master, text="Wybierz rodzaj zasobów:", font=("Arial", 14)).pack(pady=20)

        Button(master, text="Budowlane", width=20, command=self.open_construction).pack(pady=15)
        Button(master, text="Medyczne", width=20, command=self.open_medical).pack(pady=15)
        Button(master, text="Energetyczne", width=20, command=self.open_energy).pack(pady=15)
        Button(master, text="Edukacyjne", width=20, command=self.open_education).pack(pady=15)
        Button(master, text="Żywieniowe", width=20, command=self.open_food).pack(pady=15)
        Button(master, text="Wyjście", width=20, command=self.exit_app).pack(pady=15)

    def exit_app(self):
        self.master.destroy()
        self.master.quit()

    def open_construction(self):
        self.master.withdraw()
        Construction(self.master)

    def open_medical(self):
        self.master.withdraw()
        Medical(self.master)

    def open_energy(self):
        self.master.withdraw()
        Energy(self.master)

    def open_education(self):
        self.master.withdraw()
        Education(self.master)

    def open_food(self):
        self.master.withdraw()
        Food(self.master)
