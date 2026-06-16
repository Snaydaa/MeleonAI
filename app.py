import tkinter as tk
import customtkinter as ctk

from frontend.background import GalacticBackground
from frontend.styles      import Colors, Dims


class MarsAIApp:
    """Haupt-App-Controller für meleonAI."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.fenster = ctk.CTk()
        self.fenster.title("meleonAI")
        self.fenster.configure(fg_color=Colors.SPACE_BLACK)
        self.fenster.geometry("1100x800")
        self.fenster.minsize(800, 600)
        self.fenster.bind("<Control-q>", lambda e: self.beenden())
        self.fenster.update_idletasks()

        self.hintergrund_canvas = tk.Canvas(
            self.fenster,
            bg=Colors.SPACE_BLACK,
            highlightthickness=0
        )
        self.hintergrund_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.hintergrund = GalacticBackground(self.hintergrund_canvas)

        self.aktiver_screen = None

        from frontend.screens.splash import SplashScreen
        self.screen_anzeigen(SplashScreen)

    def screen_anzeigen(self, ScreenClass, **kwargs):
        print(f"\nLade Screen: {ScreenClass.__name__} ...")

        neuer_screen = ScreenClass(self.fenster, app=self, **kwargs)

        if self.aktiver_screen is None:
            neuer_screen.place(x=0, y=0, relwidth=1, relheight=1)
            neuer_screen.lift()
            self.aktiver_screen = neuer_screen
            print(f"{ScreenClass.__name__} ist jetzt aktiv.")
        else:
            self._screen_wechseln(neuer_screen)

    def _screen_wechseln(self, neuer_screen):
        alter_screen = self.aktiver_screen

        neuer_screen.place(x=0, y=0, relwidth=1, relheight=1)
        neuer_screen.lift()

        alter_screen.place_forget()
        alter_screen.destroy()

        self.aktiver_screen = neuer_screen

    def starten(self):
        self.fenster.mainloop()

    def beenden(self):
        self.hintergrund.animationen_stoppen()
        self.fenster.quit()
        self.fenster.destroy()


if __name__ == "__main__":
    print("MELEON AI MOTOR STARTET...")
    anwendung = MarsAIApp()
    anwendung.starten()
