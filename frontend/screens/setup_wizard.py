import customtkinter as ctk

from frontend.styles import Colors, Fonts, Dims


class SetupWizardScreen(ctk.CTkFrame):
    """Zwei-Schritt Setup-Wizard mit Progressive Disclosure."""

    def __init__(self, parent, app, medientyp: str = "image", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app       = app
        self.medientyp = medientyp

        # Zustand
        self.gewaehlter_umfang: str | None = None
        self.gewaehlter_modus:  str | None = None
        self._schritt2_sichtbar = False

        self._ui_aufbauen()

    def _ui_aufbauen(self):
        self._topbar_aufbauen()

        self._inhalt = ctk.CTkFrame(self, fg_color="transparent")
        self._inhalt.place(relx=0.5, rely=0.50, anchor="center")

        self._fortschritt_aufbauen()
        self._schritt1_aufbauen()
        self._schritt2_aufbauen()
        self._cta_aufbauen()

    def _topbar_aufbauen(self):
        leiste = ctk.CTkFrame(self, fg_color="transparent")
        leiste.pack(fill="x", padx=40, pady=(24, 0))

        ctk.CTkButton(
            leiste, text="←  Zurück",
            font=Fonts.SMALL_B,
            fg_color="transparent",
            hover_color=Colors.BTN_GHOST_H,
            text_color=Colors.TEXT_SECONDARY,
            border_width=1, border_color=Colors.BTN_OUTLINE,
            corner_radius=8, height=34, width=110,
            cursor="hand2",
            command=self._zurueck
        ).pack(side="left")

        logo_rahmen = ctk.CTkFrame(leiste, fg_color="transparent")
        logo_rahmen.pack(side="right")
        ctk.CTkLabel(logo_rahmen, text="mars", font=(Fonts.SANS, 16, "bold"),
                     text_color=Colors.TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(logo_rahmen, text="AI", font=(Fonts.SANS, 16, "bold"),
                     text_color=Colors.ACCENT_BRIGHT).pack(side="left")

    def _fortschritt_aufbauen(self):
        fortschritt = ctk.CTkFrame(self._inhalt, fg_color="transparent")
        fortschritt.pack(pady=(0, 36))

        schritte = ["Medientyp", "Scope", "Modus", "Workspace"]
        for i, beschriftung in enumerate(schritte):
            ist_fertig = (i == 0)
            ist_aktiv  = (i == 1)

            punkt_farbe = Colors.ACCENT if (ist_fertig or ist_aktiv) else Colors.TEXT_MUTED
            text_farbe  = Colors.TEXT_PRIMARY if ist_aktiv else (
                          Colors.TEXT_ACCENT  if ist_fertig else Colors.TEXT_MUTED)

            spalte = ctk.CTkFrame(fortschritt, fg_color="transparent")
            spalte.pack(side="left", padx=6)

            ctk.CTkFrame(spalte, fg_color=punkt_farbe,
                         width=8, height=8, corner_radius=4).pack()
            ctk.CTkLabel(spalte, text=beschriftung, font=Fonts.TINY,
                         text_color=text_farbe).pack(pady=(3, 0))

            if i < len(schritte) - 1:
                linien_farbe = Colors.ACCENT_DIM if (i == 0) else Colors.TEXT_MUTED
                ctk.CTkFrame(fortschritt, fg_color=linien_farbe,
                             width=40, height=1).pack(side="left", pady=(0, 12))

    def _schritt1_aufbauen(self):
        schritt1 = ctk.CTkFrame(self._inhalt, fg_color="transparent")
        schritt1.pack(pady=(0, 32))

        ctk.CTkLabel(
            schritt1,
            text="Schritt 1: Was genau hast du vor?",
            font=Fonts.H2,
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(0, 6))

        typ_hinweis = "Bild" if self.medientyp == "image" else "Video"
        ctk.CTkLabel(
            schritt1,
            text=f"Wähle den Umfang deiner {typ_hinweis}-Verarbeitung.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 24))

        zeile1 = ctk.CTkFrame(schritt1, fg_color="transparent")
        zeile1.pack()

        self._karte_einzeln = self._auswahl_karte_aufbauen(
            parent      = zeile1,
            symbol      = "□",
            titel       = "Einzelnes Bild" if self.medientyp == "image" else "Einzelnes Video",
            untertitel  = "Ein Medium verarbeiten",
            kennzeichen = "single",
            akzent      = Colors.ACCENT,
            deaktiviert = False,
            rueckruf    = self._bei_umfang_gewaehlt
        )

        ctk.CTkFrame(zeile1, fg_color="transparent", width=20).pack(side="left")

        self._karte_stapel = self._auswahl_karte_aufbauen(
            parent      = zeile1,
            symbol      = "⊞",
            titel       = "Batch / Diashow",
            untertitel  = "Mehrere Medien auf einmal",
            kennzeichen = "batch",
            akzent      = Colors.TEXT_MUTED,
            deaktiviert = True,
            rueckruf    = None
        )

    def _schritt2_aufbauen(self):
        # Inhalt startet unsichtbar, wird nach Schritt 1 per Animation eingeblendet.
        self._schritt2_rahmen = ctk.CTkFrame(self._inhalt, fg_color="transparent")
        self._schritt2_rahmen.pack(pady=(0, 0))

        self._schritt2_trenner = ctk.CTkFrame(
            self._schritt2_rahmen,
            fg_color=Colors.CARD_BORDER,
            height=1
        )
        self._schritt2_trenner.pack(fill="x", pady=(0, 28))
        self._schritt2_trenner.pack_forget()

        self._schritt2_inhalt = ctk.CTkFrame(self._schritt2_rahmen, fg_color="transparent")
        self._schritt2_inhalt.pack_forget()

        ctk.CTkLabel(
            self._schritt2_inhalt,
            text="Schritt 2: Wähle deinen Modus.",
            font=Fonts.H2,
            text_color=Colors.TEXT_PRIMARY
        ).pack(pady=(0, 6))

        ctk.CTkLabel(
            self._schritt2_inhalt,
            text="Wie viel Kontrolle möchtest du über die KI haben?",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 24))

        zeile2 = ctk.CTkFrame(self._schritt2_inhalt, fg_color="transparent")
        zeile2.pack()

        self._karte_einfach = self._auswahl_karte_aufbauen(
            parent      = zeile2,
            symbol      = "◈",
            titel       = "Einfach",
            untertitel  = "KI entscheidet alles",
            kennzeichen = "simple",
            akzent      = Colors.ACCENT,
            deaktiviert = False,
            rueckruf    = self._bei_modus_gewaehlt
        )

        ctk.CTkFrame(zeile2, fg_color="transparent", width=20).pack(side="left")

        self._karte_profi = self._auswahl_karte_aufbauen(
            parent      = zeile2,
            symbol      = "◉",
            titel       = "Profi",
            untertitel  = "Manuelle Prompts & Settings",
            kennzeichen = "pro",
            akzent      = "#c07aff",
            deaktiviert = False,
            rueckruf    = self._bei_modus_gewaehlt
        )

    def _cta_aufbauen(self):
        cta_bereich = ctk.CTkFrame(self._inhalt, fg_color="transparent")
        cta_bereich.pack(pady=(32, 0))

        self._cta_knopf = ctk.CTkButton(
            cta_bereich,
            text="Weiter zum Workspace  →",
            font=(Fonts.SANS, 14, "bold"),
            fg_color=Colors.BTN_OUTLINE,
            hover_color=Colors.BTN_OUTLINE,
            text_color=Colors.TEXT_MUTED,
            corner_radius=10,
            height=52,
            width=300,
            cursor="arrow",
            command=self._weiter,
            state="disabled"
        )
        self._cta_knopf.pack()

        self._cta_hinweis = ctk.CTkLabel(
            cta_bereich,
            text="Wähle erst Scope und Modus, um fortzufahren.",
            font=Fonts.TINY,
            text_color=Colors.TEXT_MUTED
        )
        self._cta_hinweis.pack(pady=(8, 0))

    def _auswahl_karte_aufbauen(
        self, parent, symbol: str, titel: str, untertitel: str,
        kennzeichen: str, akzent: str, deaktiviert: bool, rueckruf
    ) -> ctk.CTkFrame:
        KARTE_B, KARTE_H = 230, 160

        karte = ctk.CTkFrame(
            parent,
            fg_color     = Colors.CARD_BG if not deaktiviert else Colors.SPACE_DEEP,
            corner_radius= Dims.CARD_RADIUS,
            border_width = 1,
            border_color = Colors.CARD_BORDER,
            width=KARTE_B, height=KARTE_H,
            cursor       = "hand2" if not deaktiviert else "arrow"
        )
        karte.pack(side="left")
        karte.pack_propagate(False)

        inhalt = ctk.CTkFrame(karte, fg_color="transparent")
        inhalt.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            inhalt, text=symbol,
            font       = (Fonts.SANS, 30),
            text_color = akzent if not deaktiviert else Colors.TEXT_MUTED
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            inhalt, text=titel,
            font       = Fonts.BODY_B,
            text_color = Colors.TEXT_PRIMARY if not deaktiviert else Colors.TEXT_MUTED
        ).pack(pady=(0, 3))

        untertitel_text = untertitel if not deaktiviert else "Coming soon"
        ctk.CTkLabel(
            inhalt, text=untertitel_text,
            font       = Fonts.SMALL,
            text_color = Colors.TEXT_SECONDARY if not deaktiviert else Colors.TEXT_MUTED
        ).pack()

        if not deaktiviert and rueckruf:
            def _bei_maus_rein(e, c=karte, a=akzent):
                c.configure(border_color=a)

            def _bei_maus_raus(e, c=karte):
                # Wenn diese Card bereits gewaehlt, bleibt der Rahmen farbig.
                ist_gewaehlt = (
                    (kennzeichen == self.gewaehlter_umfang) or
                    (kennzeichen == self.gewaehlter_modus)
                )
                c.configure(
                    border_color=Colors.ACCENT if ist_gewaehlt else Colors.CARD_BORDER
                )

            def _bei_klick(e, k=kennzeichen, c=karte, cb=rueckruf):
                cb(k, c)

            for element in [karte, inhalt] + list(inhalt.winfo_children()):
                element.bind("<Enter>",    _bei_maus_rein)
                element.bind("<Leave>",    _bei_maus_raus)
                element.bind("<Button-1>", _bei_klick)

        return karte

    def _bei_umfang_gewaehlt(self, umfang: str, karte: ctk.CTkFrame):
        self.gewaehlter_umfang = umfang

        self._karte_einzeln.configure(
            border_color=Colors.ACCENT       if umfang == "single" else Colors.CARD_BORDER,
            fg_color    =Colors.CARD_HOVER   if umfang == "single" else Colors.CARD_BG
        )

        if not self._schritt2_sichtbar:
            self._schritt2_sichtbar = True
            self._schritt2_einblenden()

        self._cta_aktualisieren()

    def _bei_modus_gewaehlt(self, modus: str, karte: ctk.CTkFrame):
        self.gewaehlter_modus = modus

        for c, m in [(self._karte_einfach, "simple"), (self._karte_profi, "pro")]:
            c.configure(
                border_color=Colors.ACCENT     if modus == m else Colors.CARD_BORDER,
                fg_color    =Colors.CARD_HOVER if modus == m else Colors.CARD_BG
            )

        self._cta_aktualisieren()

    def _schritt2_einblenden(self):
        # Slide-Down-Animation durch schrittweises pack().
        self._schritt2_trenner.pack(fill="x", pady=(0, 28))

        schritte     = 16
        verzoegerung = 12

        def schritt_zeigen(i):
            if i == 0:
                self._schritt2_inhalt.pack()
            if i < schritte:
                self.after(verzoegerung, schritt_zeigen, i + 1)

        self.after(30, schritt_zeigen, 0)

    def _cta_aktualisieren(self):
        if self.gewaehlter_umfang and self.gewaehlter_modus:
            self._cta_knopf.configure(
                state       = "normal",
                fg_color    = Colors.ACCENT,
                hover_color = Colors.BTN_HOVER,
                text_color  = Colors.TEXT_PRIMARY,
                cursor      = "hand2"
            )
            modus_text = "Einfach" if self.gewaehlter_modus == "simple" else "Profi"
            self._cta_hinweis.configure(
                text       = f"Scope: {self.gewaehlter_umfang.capitalize()}  ·  Modus: {modus_text}",
                text_color = Colors.TEXT_ACCENT
            )

    def _weiter(self):
        if not (self.gewaehlter_umfang and self.gewaehlter_modus):
            return
        from frontend.screens.editor import EditorScreen
        self.app.screen_anzeigen(
            EditorScreen,
            medientyp = self.medientyp,
            modus     = self.gewaehlter_modus
        )

    def _zurueck(self):
        from frontend.screens.dashboard import DashboardScreen
        self.app.screen_anzeigen(DashboardScreen)
