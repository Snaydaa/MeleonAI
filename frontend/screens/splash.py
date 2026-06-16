import customtkinter as ctk
import os
from PIL import Image
from frontend.styles import Colors, Fonts, Dims


class SplashScreen(ctk.CTkFrame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app = app
        self._ui_aufbauen()

    def _ui_aufbauen(self):
        mitte = ctk.CTkFrame(self, fg_color="transparent")
        mitte.place(relx=0.5, rely=0.5, anchor="center")

        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            bildpfad = os.path.join(current_dir, "img", "logoMELION-Photoroom.png")
            rohbild = Image.open(bildpfad)
            self.logo_image = ctk.CTkImage(
                light_image=rohbild, dark_image=rohbild, size=(250, 250)
            )
            ctk.CTkLabel(mitte, image=self.logo_image, text="").pack(pady=(0, 20))
        except Exception:
            ctk.CTkLabel(
                mitte, text="marsAI",
                font=(Fonts.SANS, 64, "bold"),
                text_color=Colors.TEXT_PRIMARY
            ).pack(pady=(0, 20))

        ctk.CTkLabel(
            mitte,
            text="Your Visual Intelligence Suite",
            font=Fonts.TAGLINE,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(4, 40))

        weiter_knopf = ctk.CTkButton(
            mitte,
            text="Jetzt starten  →",
            font=Fonts.BUTTON,
            fg_color=Colors.BTN_PRIMARY,
            hover_color=Colors.BTN_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            corner_radius=Dims.BTN_RADIUS,
            height=Dims.BTN_HEIGHT,
            width=220,
            cursor="hand2",
            command=lambda: self.app.screen_anzeigen(self._login_klasse())
        )
        weiter_knopf.pack()

    def _login_klasse(self):
        from frontend.screens.login import LoginScreen
        return LoginScreen
