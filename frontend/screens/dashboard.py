import customtkinter as ctk
from frontend.styles import Colors, Fonts, Dims


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, app, benutzername="Gast", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app          = app
        self.benutzername = benutzername
        self._ui_aufbauen()

    def _ui_aufbauen(self):
        kopfbereich = ctk.CTkFrame(self, fg_color="transparent")
        kopfbereich.pack(fill="x", padx=40, pady=28)

        nutzer_rahmen = ctk.CTkFrame(
            kopfbereich,
            fg_color=Colors.CARD_BG,
            corner_radius=20,
            border_width=1,
            border_color=Colors.CARD_BORDER
        )
        nutzer_rahmen.pack(side="right")
        ctk.CTkLabel(
            nutzer_rahmen,
            text=f"  ◉  {self.benutzername}  ",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY
        ).pack(padx=12, pady=6)

        inhalt = ctk.CTkFrame(self, fg_color="transparent")
        inhalt.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inhalt,
            text="Was möchtest du erstellen?",
            font=Fonts.TITLE,
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(0, 8))
        ctk.CTkLabel(
            inhalt,
            text="Wähle deinen Medientyp -- marsAI erledigt den Rest.",
            font=Fonts.BODY,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 48))

        karten_reihe = ctk.CTkFrame(inhalt, fg_color="transparent")
        karten_reihe.pack()

        self._karte_aufbauen(
            karten_reihe, "🖼", "Bilder",
            "JPG, PNG, WEBP",
            "Analysiere und generiere\nBilder mit KI-Power.",
            "image", Colors.ACCENT
        )

        ctk.CTkFrame(karten_reihe, fg_color="transparent", width=24).pack(side="left")

        self._karte_aufbauen(
            karten_reihe, "▶", "Videos",
            "MP4, MOV, AVI",
            "KI-gestützte Bearbeitung\nund Frame-Analyse.",
            "video", "#3abeff"
        )

    def _karte_aufbauen(self, parent, symbol, titel, untertitel, beschreibung,
                        medientyp, akzent):
        karte = ctk.CTkFrame(
            parent,
            fg_color=Colors.CARD_BG,
            corner_radius=Dims.CARD_RADIUS,
            border_width=1,
            border_color=Colors.CARD_BORDER,
            width=280, height=320,
            cursor="hand2"
        )
        karte.pack(side="left")
        karte.pack_propagate(False)

        ctk.CTkLabel(karte, text=symbol, font=(Fonts.SANS, 48),
                     text_color=akzent).pack(pady=(30, 10))
        ctk.CTkLabel(karte, text=titel, font=Fonts.CARD_TITLE,
                     text_color=Colors.TEXT_PRIMARY).pack(pady=(0, 4))
        ctk.CTkLabel(karte, text=untertitel, font=Fonts.SMALL_B,
                     text_color=akzent).pack(pady=(0, 12))
        ctk.CTkLabel(karte, text=beschreibung, font=Fonts.CARD_SUB,
                     text_color=Colors.TEXT_SECONDARY, justify="center").pack()

        def bei_klick(e):
            self.app.screen_anzeigen(self._wizard_klasse(), medientyp=medientyp)

        karte.bind("<Button-1>", bei_klick)
        for child in karte.winfo_children():
            child.bind("<Button-1>", bei_klick)

    def _wizard_klasse(self):
        from frontend.screens.setup_wizard import SetupWizardScreen
        return SetupWizardScreen
