import customtkinter as ctk

from frontend.styles import Colors, Fonts, Dims


class LoginScreen(ctk.CTkFrame):
    """Login-Bildschirm: zentrierte Card, Galaxy im Hintergrund."""

    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app = app
        self._ui_aufbauen()

    def _ui_aufbauen(self):
        logo_rahmen = ctk.CTkFrame(self, fg_color="transparent")
        logo_rahmen.place(x=40, y=30)
        ctk.CTkLabel(
            logo_rahmen,
            text="mars", font=(Fonts.SANS, 18, "bold"),
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left")
        ctk.CTkLabel(
            logo_rahmen,
            text="AI", font=(Fonts.SANS, 18, "bold"),
            text_color=Colors.ACCENT_BRIGHT
        ).pack(side="left")

        karte = ctk.CTkFrame(
            self,
            fg_color=Colors.CARD_BG,
            corner_radius=Dims.CARD_RADIUS,
            border_width=1,
            border_color=Colors.CARD_BORDER,
            width=440,
            height=580
        )
        karte.place(relx=0.5, rely=0.5, anchor="center")
        karte.pack_propagate(False)

        inhalt = ctk.CTkFrame(karte, fg_color="transparent")
        inhalt.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85)

        ctk.CTkLabel(
            inhalt,
            text="Willkommen zurück",
            font=Fonts.H2,
            text_color=Colors.TEXT_PRIMARY
        ).pack(anchor="w", pady=(0, 4))

        ctk.CTkLabel(
            inhalt,
            text="Melde dich an oder teste direkt.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY
        ).pack(anchor="w", pady=(0, 28))

        ctk.CTkLabel(inhalt, text="E-Mail", font=Fonts.SMALL_B,
                     text_color=Colors.TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        self._email_eingabe = ctk.CTkEntry(
            inhalt,
            placeholder_text="name@beispiel.de",
            font=Fonts.INPUT_FONT,
            fg_color=Colors.INPUT_BG,
            border_color=Colors.INPUT_BORDER,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_MUTED,
            border_width=1,
            corner_radius=8,
            height=Dims.INPUT_HEIGHT
        )
        self._email_eingabe.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(inhalt, text="Passwort", font=Fonts.SMALL_B,
                     text_color=Colors.TEXT_SECONDARY).pack(anchor="w", pady=(0, 5))
        self._passwort_eingabe = ctk.CTkEntry(
            inhalt,
            placeholder_text="••••••••",
            show="•",
            font=Fonts.INPUT_FONT,
            fg_color=Colors.INPUT_BG,
            border_color=Colors.INPUT_BORDER,
            text_color=Colors.TEXT_PRIMARY,
            placeholder_text_color=Colors.TEXT_MUTED,
            border_width=1,
            corner_radius=8,
            height=Dims.INPUT_HEIGHT
        )
        self._passwort_eingabe.pack(fill="x", pady=(0, 22))

        ctk.CTkButton(
            inhalt,
            text="Anmelden",
            font=Fonts.BUTTON,
            fg_color=Colors.BTN_PRIMARY,
            hover_color=Colors.BTN_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            corner_radius=8,
            height=Dims.BTN_HEIGHT,
            cursor="hand2",
            command=self._bei_login
        ).pack(fill="x", pady=(0, 12))

        trenner_zeile = ctk.CTkFrame(inhalt, fg_color="transparent")
        trenner_zeile.pack(fill="x", pady=(0, 12))
        ctk.CTkFrame(trenner_zeile, fg_color=Colors.CARD_BORDER,
                     height=1).pack(side="left", expand=True, fill="x")
        ctk.CTkLabel(trenner_zeile, text="  oder  ", font=Fonts.SMALL,
                     text_color=Colors.TEXT_MUTED).pack(side="left")
        ctk.CTkFrame(trenner_zeile, fg_color=Colors.CARD_BORDER,
                     height=1).pack(side="left", expand=True, fill="x")

        ctk.CTkButton(
            inhalt,
            text="Mit Google verbinden",
            font=Fonts.LABEL,
            fg_color="transparent",
            hover_color=Colors.BTN_GHOST_H,
            text_color=Colors.TEXT_SECONDARY,
            border_width=1,
            border_color=Colors.BTN_OUTLINE,
            corner_radius=8,
            height=42,
            cursor="hand2",
            command=self._bei_google_login
        ).pack(fill="x", pady=(0, 10))

        ctk.CTkFrame(inhalt, fg_color=Colors.ACCENT_DIM, height=1).pack(
            fill="x", pady=(8, 14)
        )
        ctk.CTkLabel(
            inhalt,
            text="Kein Konto? Direkt loslegen:",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 8))

        gast_knopf = ctk.CTkButton(
            inhalt,
            text="✦  Als Gast testen  →",
            font=(Fonts.SANS, 14, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.BTN_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            corner_radius=8,
            height=50,
            cursor="hand2",
            command=self._bei_gast_login
        )
        gast_knopf.pack(fill="x")

        ctk.CTkLabel(
            self,
            text="Durch die Nutzung stimmst du unseren Nutzungsbedingungen zu.",
            font=Fonts.TINY,
            text_color=Colors.TEXT_MUTED
        ).place(relx=0.5, rely=0.96, anchor="center")

    def _bei_login(self):
        print("[Login] E-Mail Login nicht implementiert (Demo).")

    def _bei_google_login(self):
        print("[Login] Google Login nicht implementiert (Demo).")

    def _bei_gast_login(self):
        from frontend.screens.dashboard import DashboardScreen
        self.app.screen_anzeigen(DashboardScreen, benutzername="Gast")
