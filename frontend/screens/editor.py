import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
import threading
import traceback

from frontend.styles import Colors, Fonts, Dims

SCHNELLAKTIONEN = [
    ("Text übersetzen  (EN → DE)",
     "Englischen Text im Bild auf Deutsch übersetzen",
     "Translate all visible text from English to German, keeping the original style and layout."),

    ("Wasserzeichen entfernen",
     "Sichtbare Wasserzeichen möglichst unsichtbar machen",
     "Remove any visible watermarks or logos from the image seamlessly."),

    ("Hintergrund entfernen",
     "Hintergrund transparent / weiß ersetzen",
     "Remove the background from the image and make it transparent."),

    ("Objekte erkennen & beschriften",
     "KI analysiert und beschriftet Objekte im Bild",
     "Identify and label all prominent objects in the image."),

    ("Stil anpassen  (realistisch → Illustration)",
     "Visuellen Stil des Bildes transformieren",
     "Transform the image style into a clean modern illustration while preserving the content."),

    ("Text-Layout verbessern",
     "Typografie und Lesbarkeit optimieren",
     "Improve the text layout and typography for better readability and visual appeal."),
]


class EditorScreen(ctk.CTkFrame):
    """Haupteditor: Medien-Import, KI-Analyse und Generierung."""

    def __init__(self, parent, app, medientyp: str = "image", modus: str = "simple", **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app       = app
        self.medientyp = medientyp

        self._medienpfad:        Path | None    = None
        self._vorschaubild                      = None
        self._verarbeitet:       bool           = False
        self._checkbox_variablen: list[tk.BooleanVar] = []

        self._ui_aufbauen()

    def _ui_aufbauen(self):
        self._topbar_aufbauen()

        haupt = ctk.CTkFrame(self, fg_color="transparent")
        haupt.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        haupt.columnconfigure(0, weight=6)
        haupt.columnconfigure(1, weight=1)
        haupt.columnconfigure(2, weight=4)
        haupt.rowconfigure(0, weight=1)

        links = ctk.CTkFrame(
            haupt,
            fg_color=Colors.CARD_BG,
            corner_radius=Dims.CARD_RADIUS,
            border_width=1,
            border_color=Colors.CARD_BORDER
        )
        links.grid(row=0, column=0, sticky="nsew")
        self._linkes_panel_aufbauen(links)

        ctk.CTkFrame(haupt, fg_color="transparent", width=16).grid(row=0, column=1)

        rechts = ctk.CTkFrame(
            haupt,
            fg_color=Colors.CARD_BG,
            corner_radius=Dims.CARD_RADIUS,
            border_width=1,
            border_color=Colors.CARD_BORDER
        )
        rechts.grid(row=0, column=2, sticky="nsew")
        self._rechtes_panel_aufbauen(rechts)

    def _topbar_aufbauen(self):
        leiste = ctk.CTkFrame(self, fg_color="transparent")
        leiste.pack(fill="x", padx=24, pady=(20, 14))

        ctk.CTkButton(
            leiste,
            text="←  Zurück",
            font=Fonts.SMALL_B,
            fg_color="transparent",
            hover_color=Colors.BTN_GHOST_H,
            text_color=Colors.TEXT_SECONDARY,
            border_width=1,
            border_color=Colors.BTN_OUTLINE,
            corner_radius=8,
            height=34,
            width=110,
            cursor="hand2",
            command=self._zurueck
        ).pack(side="left")

        titel_text = "Bild-Editor" if self.medientyp == "image" else "Video-Editor"
        ctk.CTkLabel(
            leiste,
            text=titel_text,
            font=Fonts.H3,
            text_color=Colors.TEXT_PRIMARY
        ).pack(side="left", padx=20)

        logo_zeile = ctk.CTkFrame(leiste, fg_color="transparent")
        logo_zeile.pack(side="right")
        ctk.CTkLabel(logo_zeile, text="mars", font=(Fonts.SANS, 16, "bold"),
                     text_color=Colors.TEXT_PRIMARY).pack(side="left")
        ctk.CTkLabel(logo_zeile, text="AI", font=(Fonts.SANS, 16, "bold"),
                     text_color=Colors.ACCENT_BRIGHT).pack(side="left")

    def _linkes_panel_aufbauen(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self._ablage_rahmen = ctk.CTkFrame(parent, fg_color="transparent")
        self._ablage_rahmen.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self._ablage_rahmen.columnconfigure(0, weight=1)
        self._ablage_rahmen.rowconfigure(0, weight=1)

        self._ablage_anzeigen()

        untere_leiste = ctk.CTkFrame(parent, fg_color=Colors.SPACE_DEEP,
                                     corner_radius=0, height=46)
        untere_leiste.grid(row=1, column=0, sticky="ew")
        untere_leiste.grid_propagate(False)
        untere_leiste.columnconfigure(0, weight=1)

        self._dateiname_label = ctk.CTkLabel(
            untere_leiste,
            text="Keine Datei geladen",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        )
        self._dateiname_label.grid(row=0, column=0, padx=16, sticky="w")

        ctk.CTkButton(
            untere_leiste,
            text="+ Neu",
            font=Fonts.SMALL_B,
            fg_color="transparent",
            hover_color=Colors.BTN_GHOST_H,
            text_color=Colors.ACCENT,
            width=60, height=30,
            cursor="hand2",
            command=self._medium_laden
        ).grid(row=0, column=1, padx=10)

    def _ablage_anzeigen(self):
        for w in self._ablage_rahmen.winfo_children():
            w.destroy()

        ablage_typ    = "Bild"  if self.medientyp == "image" else "Video"
        format_hinweis = "(JPG · PNG · WEBP)" if self.medientyp == "image" else "(MP4 · MOV · AVI)"

        ablage_zone = ctk.CTkFrame(
            self._ablage_rahmen,
            fg_color=Colors.SPACE_DEEP,
            corner_radius=12,
            border_width=2,
            border_color=Colors.CARD_BORDER,
            cursor="hand2"
        )
        ablage_zone.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        ablage_zone.columnconfigure(0, weight=1)
        ablage_zone.rowconfigure(0, weight=1)

        inhalt = ctk.CTkFrame(ablage_zone, fg_color="transparent")
        inhalt.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inhalt, text="⊕", font=(Fonts.SANS, 42),
                     text_color=Colors.ACCENT_DIM).pack(pady=(0, 12))
        ctk.CTkLabel(
            inhalt,
            text=f"{ablage_typ} hierher ziehen",
            font=Fonts.H3,
            text_color=Colors.TEXT_SECONDARY
        ).pack(pady=(0, 6))
        ctk.CTkLabel(inhalt, text=format_hinweis, font=Fonts.SMALL,
                     text_color=Colors.TEXT_MUTED).pack(pady=(0, 20))
        ctk.CTkButton(
            inhalt,
            text="Datei auswählen",
            font=Fonts.BUTTON,
            fg_color=Colors.BTN_PRIMARY,
            hover_color=Colors.BTN_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            corner_radius=8,
            height=42,
            width=180,
            cursor="hand2",
            command=self._medium_laden
        ).pack()

    def _vorschau_anzeigen(self, pfad: Path):
        for w in self._ablage_rahmen.winfo_children():
            w.destroy()

        if self.medientyp == "image":
            self._bild_vorschau_anzeigen(pfad)
        else:
            self._video_platzhalter_anzeigen(pfad)

    def _bild_vorschau_anzeigen(self, pfad: Path):
        try:
            from PIL import Image
            bild = Image.open(pfad)
            bild.thumbnail((600, 500), Image.Resampling.LANCZOS)

            self._vorschaubild = ctk.CTkImage(
                light_image=bild,
                dark_image=bild,
                size=(bild.width, bild.height)
            )

            lbl = ctk.CTkLabel(
                self._ablage_rahmen,
                image=self._vorschaubild,
                text=""
            )
            lbl.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        except Exception as e:
            self._ablage_anzeigen()
            print(f"[Vorschau] Fehler beim Laden: {e}")

    def _video_platzhalter_anzeigen(self, pfad: Path):
        rahmen = ctk.CTkFrame(self._ablage_rahmen, fg_color="transparent")
        rahmen.grid(row=0, column=0, sticky="nsew")
        rahmen.columnconfigure(0, weight=1)
        rahmen.rowconfigure(0, weight=1)

        inhalt = ctk.CTkFrame(rahmen, fg_color="transparent")
        inhalt.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(inhalt, text="▶", font=(Fonts.SANS, 48),
                     text_color="#3abeff").pack()
        ctk.CTkLabel(inhalt, text=pfad.name, font=Fonts.BODY,
                     text_color=Colors.TEXT_PRIMARY).pack(pady=8)
        ctk.CTkLabel(inhalt, text="Video geladen -- bereit für Analyse",
                     font=Fonts.SMALL, text_color=Colors.TEXT_SECONDARY).pack()

    def _rechtes_panel_aufbauen(self, parent):
        scroll_bereich = ctk.CTkScrollableFrame(
            parent,
            fg_color="transparent",
            scrollbar_button_color=Colors.CARD_BORDER,
            scrollbar_button_hover_color=Colors.ACCENT_DIM
        )
        scroll_bereich.pack(fill="both", expand=True, padx=4, pady=4)

        abstand = {"padx": 20}

        self._abschnitts_titel(scroll_bereich, "① Analysieren", abstand)

        ctk.CTkLabel(
            scroll_bereich,
            text="Die KI analysiert dein Medium und extrahiert\n"
                 "Texte, Objekte und Kontext automatisch.",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED,
            justify="left"
        ).pack(anchor="w", pady=(0, 12), **abstand)

        self._analyse_box = ctk.CTkTextbox(
            scroll_bereich,
            height=80,
            font=Fonts.MONO,
            fg_color=Colors.INPUT_BG,
            border_color=Colors.INPUT_BORDER,
            border_width=1,
            text_color=Colors.TEXT_SECONDARY,
            state="disabled"
        )
        self._analyse_box.pack(fill="x", pady=(0, 16), **abstand)
        self._analyse_platzhalter_setzen()

        self._abschnitts_titel(scroll_bereich, "② Quick-Actions", abstand)

        ctk.CTkLabel(
            scroll_bereich,
            text="Aktiviere vorgefertigte Aktionen:",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 10), **abstand)

        self._checkbox_variablen.clear()
        for beschriftung, _, __ in SCHNELLAKTIONEN:
            variable = tk.BooleanVar(value=False)
            self._checkbox_variablen.append(variable)
            checkbox = ctk.CTkCheckBox(
                scroll_bereich,
                text=beschriftung,
                font=Fonts.SMALL,
                variable=variable,
                fg_color=Colors.ACCENT,
                hover_color=Colors.BTN_HOVER,
                border_color=Colors.CARD_BORDER,
                text_color=Colors.TEXT_SECONDARY,
                checkmark_color=Colors.TEXT_PRIMARY,
                cursor="hand2"
            )
            checkbox.pack(anchor="w", pady=4, **abstand)

        ctk.CTkFrame(scroll_bereich, fg_color=Colors.CARD_BORDER, height=1).pack(
            fill="x", pady=16, **abstand)

        self._abschnitts_titel(scroll_bereich, "③ Eigener Prompt", abstand)

        ctk.CTkLabel(
            scroll_bereich,
            text="Beschreibe, was die KI tun soll:",
            font=Fonts.SMALL,
            text_color=Colors.TEXT_MUTED
        ).pack(anchor="w", pady=(0, 8), **abstand)

        self._eingabe_feld = ctk.CTkTextbox(
            scroll_bereich,
            height=110,
            font=Fonts.INPUT_FONT,
            fg_color=Colors.INPUT_BG,
            border_color=Colors.INPUT_BORDER,
            border_width=1,
            text_color=Colors.TEXT_PRIMARY
        )
        self._eingabe_feld.pack(fill="x", pady=(0, 16), **abstand)
        self._eingabe_feld.insert(
            "0.0",
            "z. B. Übersetze den Text auf Deutsch und behalte\n"
            "das ursprüngliche Layout und den Stil bei."
        )

        ctk.CTkFrame(scroll_bereich, fg_color=Colors.CARD_BORDER, height=1).pack(
            fill="x", pady=(0, 16), **abstand)

        self._generier_knopf = ctk.CTkButton(
            scroll_bereich,
            text="✦  Analysieren & Generieren",
            font=(Fonts.SANS, 14, "bold"),
            fg_color=Colors.ACCENT,
            hover_color=Colors.BTN_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            corner_radius=10,
            height=52,
            cursor="hand2",
            command=self._pipeline_starten
        )
        self._generier_knopf.pack(fill="x", pady=(0, 8), **abstand)

    def _abschnitts_titel(self, parent, text: str, pack_kwargs: dict):
        ctk.CTkLabel(
            parent,
            text=text,
            font=Fonts.BODY_B,
            text_color=Colors.TEXT_ACCENT
        ).pack(anchor="w", pady=(14, 4), **pack_kwargs)

    def _analyse_platzhalter_setzen(self):
        self._analyse_box.configure(state="normal")
        self._analyse_box.delete("0.0", "end")
        self._analyse_box.insert("0.0", "KI-Analyse erscheint hier nach dem Start ...")
        self._analyse_box.configure(state="disabled")

    def _analyse_aktualisieren(self, text: str):
        self._analyse_box.configure(state="normal")
        self._analyse_box.delete("0.0", "end")
        self._analyse_box.insert("0.0", text)
        self._analyse_box.configure(state="disabled")

    def _aktiven_prompt_holen(self) -> str:
        teile = []
        for i, (_, _, snippet) in enumerate(SCHNELLAKTIONEN):
            if self._checkbox_variablen[i].get():
                teile.append(snippet)
        eigener_text = self._eingabe_feld.get("0.0", "end").strip()
        if eigener_text:
            teile.append(eigener_text)
        return " ".join(teile) if teile else "Analysiere und beschreibe das Bild."

    def _pipeline_starten(self):
        if self._verarbeitet:
            return
        if self._medienpfad is None:
            self._analyse_aktualisieren("Bitte zuerst eine Datei laden.")
            return

        self._verarbeitet = True
        self._generier_knopf.configure(
            text="Verarbeite ... (Kann 10-20 Sek. dauern)",
            state="disabled",
            fg_color=Colors.ACCENT_DIM
        )
        self._analyse_aktualisieren("Kontaktiere OpenAI... Bitte warten.")

        eingabe = self._aktiven_prompt_holen()
        threading.Thread(
            target=self._backend_aufrufen, args=(eingabe,), daemon=True
        ).start()

    def _backend_aufrufen(self, eingabe: str):
        try:
            from backend.processor import MarsProcessor
            ergebnis = MarsProcessor.verarbeiten(
                medienpfad=self._medienpfad,
                eingabe=eingabe,
                medientyp=self.medientyp
            )
            # GUI-Updates nur im Main-Thread via after()
            self.after(0, lambda: self._analyse_aktualisieren(
                ergebnis.get("analysis", "Keine Analyse verfügbar.")
            ))
        except Exception as e:
            print("\nHINWEIS: Die API hat einen Fehler gemeldet:")
            traceback.print_exc()
            print("------------------------------------------------\n")
            fehlermeldung = f"Fehler: {e}\n(Siehe Terminal für Details)"
            self.after(0, lambda: self._analyse_aktualisieren(fehlermeldung))
        finally:
            self.after(0, self._ui_zuruecksetzen)

    def _ui_zuruecksetzen(self):
        self._verarbeitet = False
        self._generier_knopf.configure(
            text="✦  Analysieren & Generieren",
            state="normal",
            fg_color=Colors.ACCENT
        )

    def _medium_laden(self):
        if self.medientyp == "image":
            dateitypen = [
                ("Bilder", "*.jpg *.jpeg *.png *.webp *.bmp *.gif"),
                ("Alle Dateien", "*.*")
            ]
        else:
            dateitypen = [
                ("Videos", "*.mp4 *.mov *.avi *.mkv"),
                ("Alle Dateien", "*.*")
            ]

        pfad_str = filedialog.askopenfilename(
            title="Medium auswählen",
            filetypes=dateitypen
        )
        if not pfad_str:
            return

        self._medienpfad = Path(pfad_str)
        self._dateiname_label.configure(text=self._medienpfad.name)
        self._vorschau_anzeigen(self._medienpfad)

    def _zurueck(self):
        from frontend.screens.dashboard import DashboardScreen
        self.app.screen_anzeigen(DashboardScreen)
