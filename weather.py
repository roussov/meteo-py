import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Combobox, Frame
from tkinter import Text
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Liste de villes fictives
villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]

# Génération de données météo réalistes
def simuler_meteo(ville):
    saison = "été" if 4 <= datetime.datetime.now().month <= 9 else "hiver"
    base_temp = {"été": random.randint(24, 30), "hiver": random.randint(2, 10)}

    previsions = []
    for i in range(7):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        temp = base_temp[saison] + random.randint(-3, 3)
        humidite = random.randint(50, 90)
        pression = random.randint(990, 1035)
        vent = random.randint(5, 25)
        condition = random.choice(["☀️ Soleil", "🌧️ Pluie", "⛅ Nuages", "⛈️ Orage", "🌫️ Brume"])
        previsions.append({
            "date": date.strftime("%a %d/%m"),
            "temp": temp,
            "humidite": humidite,
            "pression": pression,
            "vent": vent,
            "condition": condition
        })
    return previsions

# Application principale
class ApplicationMeteo:
    def __init__(self, master):
        self.master = master
        self.master.title("🌤️ Station Météo Locale - Simulation")
        self.style = Style(theme="flatly")

        # --- En-tête & Sélecteur ---
        top_frame = Frame(master, padding=10)
        top_frame.pack(fill="x")

        tk.Label(top_frame, text="Choisir une ville :", font=("Helvetica", 12)).pack(side="left")
        self.ville_var = tk.StringVar(value=villes[0])
        self.combo = Combobox(top_frame, textvariable=self.ville_var, values=villes, bootstyle="info", width=20)
        self.combo.pack(side="left", padx=10)
        self.combo.bind("<<ComboboxSelected>>", self.mettre_a_jour)

        # --- Zone d'affichage texte météo ---
        self.texte = Text(master, height=10, font=("Consolas", 11), bg="#f8f9fa", bd=0)
        self.texte.pack(fill="x", padx=10, pady=5)

        # --- Zone graphique météo ---
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(pady=10)

        self.mettre_a_jour()

    def mettre_a_jour(self, event=None):
        ville = self.ville_var.get()
        self.data = simuler_meteo(ville)
        self.afficher_texte()
        self.afficher_graphique()

    def afficher_texte(self):
        self.texte.delete("1.0", tk.END)
        for jour in self.data:
            ligne = f"{jour['date']}  |  {jour['condition']}  |  🌡 {jour['temp']}°C  |  💧 {jour['humidite']}%  |  🌀 {jour['vent']} km/h\n"
            self.texte.insert(tk.END, ligne)

    def afficher_graphique(self):
        self.ax.clear()
        dates = [j["date"] for j in self.data]
        temp = [j["temp"] for j in self.data]
        hum = [j["humidite"] for j in self.data]
        press = [j["pression"] for j in self.data]

        self.ax.plot(dates, temp, label="Température (°C)", marker='o', color="tomato")
        self.ax.plot(dates, hum, label="Humidité (%)", linestyle="--", marker='x', color="skyblue")
        self.ax.plot(dates, press, label="Pression (hPa)", linestyle=":", color="gray")
        self.ax.set_title(f"Prévisions pour {self.ville_var.get()}", fontsize=12)
        self.ax.set_ylabel("Valeurs")
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()
        self.fig.tight_layout()
        self.canvas.draw()

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationMeteo(root)
    root.mainloop()
