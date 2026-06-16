import tkinter as tk
import random
import math


class GalacticBackground:
    """Modernes AI Particle Network (Web-Style) für Tkinter."""

    def __init__(self, canvas: tk.Canvas):
        self.leinwand = canvas
        self.breite   = 1100
        self.hoehe    = 800
        self._animiert = True
        self.partikel  = []
        self.leinwand.bind("<Configure>", self._bei_groessen_aenderung)
        self.zeichnen()

    def _bei_groessen_aenderung(self, ereignis):
        if ereignis.width != self.breite or ereignis.height != self.hoehe:
            self.breite, self.hoehe = ereignis.width, ereignis.height
            if hasattr(self, "_groessen_job"):
                self.leinwand.after_cancel(self._groessen_job)
            self._groessen_job = self.leinwand.after(200, self.zeichnen)

    def zeichnen(self):
        self.leinwand.delete("all")
        self.leinwand.create_rectangle(
            0, 0, self.breite, self.hoehe,
            fill="#030712", outline="", tags="bg"
        )

        # 45 Partikel für flüssige Performance
        if not self.partikel:
            for _ in range(45):
                self._partikel_erzeugen()

        if self._animiert:
            self.animieren()

    def _partikel_erzeugen(self):
        x  = random.uniform(0, self.breite)
        y  = random.uniform(0, self.hoehe)
        vx = random.uniform(-0.8, 0.8)
        vy = random.uniform(-0.8, 0.8)
        self.partikel.append({"x": x, "y": y, "vx": vx, "vy": vy})

    def animieren(self):
        if not self._animiert:
            return
        self.leinwand.delete("network")

        # Positionen aktualisieren
        for p in self.partikel:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["x"] <= 0 or p["x"] >= self.breite:
                p["vx"] *= -1
            if p["y"] <= 0 or p["y"] >= self.hoehe:
                p["vy"] *= -1

        # Verbindungen zeichnen
        max_abstand = 140

        for i, p1 in enumerate(self.partikel):
            self.leinwand.create_oval(
                p1["x"] - 2, p1["y"] - 2,
                p1["x"] + 2, p1["y"] + 2,
                fill="#2b5eff", outline="", tags="network"
            )
            for p2 in self.partikel[i + 1:]:
                abstand = math.hypot(p2["x"] - p1["x"], p2["y"] - p1["y"])
                if abstand < max_abstand:
                    helligkeit = int(255 * (1 - (abstand / max_abstand)))
                    farbe = (
                        f"#{int(43  * (helligkeit / 255)):02x}"
                        f"{int(94  * (helligkeit / 255)):02x}"
                        f"{int(255 * (helligkeit / 255)):02x}"
                    )
                    self.leinwand.create_line(
                        p1["x"], p1["y"], p2["x"], p2["y"],
                        fill=farbe, width=1, tags="network"
                    )

        # 30ms Frame-Delay (~30 FPS)
        self.leinwand.after(30, self.animieren)

    def animationen_stoppen(self):
        self._animiert = False
