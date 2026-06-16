# ══════════════════════════════════════════════════════════════════════
#  marsAI — Design System  |  styles.py
#  Alle Farben, Schriften und Layout-Konstanten zentral an einem Ort.
# ══════════════════════════════════════════════════════════════════════


class Colors:
    # ── Hintergründe ──────────────────────────────────────────────────
    SPACE_BLACK   = "#000008"   # Tiefstes Schwarz
    SPACE_DEEP    = "#03071a"   # Fast schwarz, minimal blau
    SPACE_NAVY    = "#08122e"   # Dunkelblau
    SPACE_BLUE    = "#0d1b4b"   # Mittleres Marineblau

    # ── Planet (Radial-Gradient, innen → außen) ───────────────────────
    PLANET_CORE   = "#4a28a8"   # Heller Kern
    PLANET_MID    = "#2b1570"   # Mittlerer Mantel
    PLANET_OUTER  = "#180c48"   # Äußerer Rand
    PLANET_GLOW   = "#0f0835"   # Atmosphären-Glow

    # ── UI-Akzente ────────────────────────────────────────────────────
    ACCENT        = "#2b5eff"   # Primärblau
    ACCENT_BRIGHT = "#5b8aff"   # Helles Akzentblau
    ACCENT_GLOW   = "#a3bfff"   # Leuchteffekt
    ACCENT_DIM    = "#1a3a8a"   # Gedecktes Akzentblau

    # ── Text ──────────────────────────────────────────────────────────
    TEXT_PRIMARY  = "#edf0ff"   # Haupttext
    TEXT_SECONDARY= "#7a9cc5"   # Sekundärtext
    TEXT_MUTED    = "#3a5272"   # Gedämpfter Text
    TEXT_ACCENT   = "#7aabff"   # Akzent-Text

    # ── Karten & Panels ───────────────────────────────────────────────
    CARD_BG       = "#060d22"   # Hintergrund dunkler Karten
    CARD_HOVER    = "#0a1530"   # Hover-Zustand
    CARD_BORDER   = "#1a2f60"   # Rahmen
    CARD_BORDER_H = "#2b5eff"   # Rahmen hover

    # ── Buttons ───────────────────────────────────────────────────────
    BTN_PRIMARY   = "#1a3ccc"
    BTN_HOVER     = "#2b5eff"
    BTN_OUTLINE   = "#1a2f60"
    BTN_GHOST_H   = "#0d1a3d"

    # ── Inputs ────────────────────────────────────────────────────────
    INPUT_BG      = "#050c1e"
    INPUT_BORDER  = "#1a2f60"
    INPUT_FOCUS   = "#2b5eff"

    # ── Sterne ────────────────────────────────────────────────────────
    STAR_BRIGHT   = "#e0eaff"
    STAR_DIM      = "#3a5070"
    STAR_BLUE     = "#7ab2ff"


class Fonts:
    """Font-Definitionen als Tupel für tkinter/customtkinter."""
    # Font-Familie mit Fallbacks
    SANS = "Helvetica Neue"

    # Varianten (Familie, Größe[, Stil])
    HERO         = (SANS, 64, "bold")
    HERO_THIN    = (SANS, 60)
    TITLE        = (SANS, 34, "bold")
    H2           = (SANS, 22, "bold")
    H3           = (SANS, 17)
    BODY         = (SANS, 14)
    BODY_B       = (SANS, 14, "bold")
    SMALL        = (SANS, 11)
    SMALL_B      = (SANS, 11, "bold")
    TINY         = (SANS, 9)
    BUTTON       = (SANS, 13, "bold")
    LABEL        = (SANS, 12)
    TAGLINE      = (SANS, 15)
    CARD_TITLE   = (SANS, 20, "bold")
    CARD_SUB     = (SANS, 13)
    INPUT_FONT   = (SANS, 13)
    MONO         = ("Courier New", 12)


class Dims:
    """Layout-Maße & Animations-Parameter."""
    CORNER_RADIUS   = 14
    CARD_RADIUS     = 16
    CARD_PAD        = 32
    GAP             = 16

    BTN_HEIGHT      = 48
    BTN_RADIUS      = 10
    INPUT_HEIGHT    = 46

    # Übergänge
    SLIDE_STEPS     = 28    # Anzahl Animations-Frames
    SLIDE_DELAY_MS  = 9     # ms pro Frame → ~252 ms gesamt