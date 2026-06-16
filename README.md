# meleonAI

meleonAI ist ein Python-Projekt zum Übersetzen und Bearbeiten von Texten in Bildern.

Die Idee kam aus einem einfachen Problem: Ich wollte fremdsprachige Grafiken übersetzen, ohne jedes Bild komplett manuell nachzubauen. Am Anfang dachte ich noch, dass ein guter Prompt vielleicht reicht: Bild rein, Zielvorgabe rein, fertiges Ergebnis raus.

In der Praxis war es deutlich komplizierter.

Ich habe sehr viele verschiedene Prompts ausprobiert und dabei gemerkt, dass die KI zwar viel erkennt, aber nicht automatisch so arbeitet, wie ein Programm es braucht. Mal war die Ausgabe nicht sauber als JSON formatiert, mal wurden Texte zu frei interpretiert, mal waren Layout-Informationen unbrauchbar oder die Antwort war für den nächsten Verarbeitungsschritt nicht stabil genug.

Dadurch ist nach und nach die Idee entstanden, den Ablauf in mehrere Phasen aufzuteilen: Eine Phase analysiert das Bild, eine zweite kümmert sich um die Textanpassung und danach werden die Daten wieder zusammengeführt.

So sind die Phasen `Scout`, `Artist` und `Renderer` entstanden.

Python war für mich bei diesem Projekt noch Neuland. Ich habe viel über Dateien, API-Aufrufe, JSON-Strukturen, Bilddaten und Fehlerbehandlung gelernt. Besonders hängen geblieben ist, dass jede API etwas anders arbeitet. Manche Modelle liefern Text, andere arbeiten mit Bildern, manche brauchen Base64-Daten, andere erwarten andere Formate oder reagieren sehr empfindlich auf die genaue Prompt-Struktur.

Ich hatte zwischendurch auch überlegt, ob ich bestimmte Bildbearbeitungsschritte selbst mit Bibliotheken wie Pillow lösen sollte. Das ist aber nicht der eigentliche Schwerpunkt des Projekts geworden. Der Hauptteil war für mich die Frage, wie ich KI-Ausgaben so strukturiere, dass mein Programm damit weiterarbeiten kann.

Der aktuelle lokale Workflow läuft bereits stabil. Trotzdem ist das Projekt noch Work in Progress, weil ich es weiter ausbauen und die Bedienung verbessern möchte.

## Was das Programm macht

meleonAI analysiert ein Bild, erkennt sichtbare Texte und erstellt daraus strukturierte JSON-Daten. Danach werden die erkannten Inhalte für eine Übersetzung oder Weiterverarbeitung vorbereitet.

Der grobe Ablauf:

1. Bild auswählen
2. Bild für die API vorbereiten
3. Text und Layout im Bild erkennen
4. Erkannte Texte übersetzen oder anpassen
5. Analyse und Änderungen als JSON zusammenführen
6. Ergebnis im Workflow anzeigen bzw. weiterverarbeiten

In meiner Portfolio-Version zeige ich den Workflow als Vorher/Nachher-Projekt. Ziel ist es, fremdsprachige Grafiken möglichst sauber zu lokalisieren, ohne das ursprüngliche Design komplett zu zerstören.

## Aufbau

```text
app.py              Startet die Anwendung
processor.py        Hauptlogik für Analyse, API-Aufrufe und JSON-Verarbeitung
background.py       Animierter Hintergrund für die Oberfläche
styles.py           Farben, Schriften und Layout-Konstanten
editor.py           Editor-Screen mit Upload, Quick-Actions und Promptfeld
setup_wizard.py     Geführter Einstieg für Medientyp und Modus
```

## Pipeline

Das Projekt ist in mehrere Phasen aufgeteilt, weil ein einzelner Prompt für das Ziel nicht zuverlässig genug war.

### Phase 0: Vorbereitung

Das Bild wird für die Verarbeitung vorbereitet. Dabei geht es vor allem darum, die Datei in ein Format zu bringen, das sauber an die API übergeben werden kann.

### Phase 1: Scout

Die Scout-Phase analysiert das Bild. Sie soll sichtbare Texte, Lesereihenfolge, Sprache, Koordinaten und einfache Layout-Informationen erkennen.

Wichtig war hier: Die KI soll in dieser Phase noch nichts übersetzen oder frei umformulieren. Sie soll nur möglichst strukturiert beschreiben, was im Bild sichtbar ist.

### Phase 2: Artist

Die Artist-Phase bekommt die erkannten Texte und erstellt daraus passende Änderungen oder Übersetzungen. Dabei soll der neue Text möglichst zum ursprünglichen Stil und zur vorhandenen Textfläche passen.

### Phase 2.5: Delta-Patch

In dieser Zwischenphase werden die ursprünglichen Analyse-Daten und die neuen Textdaten zusammengeführt. Die Idee dahinter ist, Analyse und Änderung getrennt zu halten, damit der Ablauf nachvollziehbarer bleibt.

### Phase 3: Renderer

Der Renderer führt die Ergebnisse aus den vorherigen Schritten zusammen und bereitet das finale Ergebnis für die Ausgabe vor.

Dieser Teil ist der Bereich, den ich perspektivisch noch weiter ausbauen möchte, zum Beispiel mit mehr Export-Optionen und besserer Kontrolle über das Endergebnis.

## Voraussetzungen

* Python 3
* OpenAI API-Key
* Abhängigkeiten wie:

  * `openai`
  * `python-dotenv`
  * `customtkinter`

Beispiel:

```bash
pip install openai python-dotenv customtkinter
```

Für den API-Key wird eine `.env` oder `schluessel.env` verwendet:

```text
OPENAI_API_KEY=sk-...
```

## Starten

Je nach Projektstruktur kann die App über die Hauptdatei gestartet werden:

```bash
python app.py
```

## Verwendete Technik

* Python
* tkinter / customtkinter für die Oberfläche
* OpenAI API für Bildanalyse und Textverarbeitung
* JSON als Austauschformat zwischen den Verarbeitungsschritten
* Base64-Bilddaten für API-Anfragen

## KI-Nutzung

In diesem Projekt ist KI nicht nur ein Hilfsmittel, sondern ein bewusster Teil der Anwendung.

Die OpenAI API wird genutzt, um Bildinhalte zu analysieren, Texte zu erkennen und strukturierte Daten zu erzeugen. Besonders die Prompts für Scout und Artist sind ein zentraler Bestandteil des Projekts, weil das Programm auf möglichst stabile JSON-Ausgaben angewiesen ist.

Ich habe viele Prompt-Versionen ausprobiert und die Struktur immer wieder angepasst. Dabei ging es nicht darum, einfach nur „mach mir das Bild auf Deutsch“ zu sagen, sondern die Aufgabe so aufzuteilen, dass mein Code mit den Zwischenergebnissen arbeiten kann.

Da Python für mich bei diesem Projekt neu war, habe ich KI auch punktuell als Lernhilfe genutzt. Vor allem bei API-Aufrufen, JSON-Strukturen, Fehlermeldungen und beim Aufräumen einzelner Codebereiche.

Die Idee, der Workflow, die Oberfläche, die Phasenlogik und die Weiterentwicklung stammen aus meinem eigenen Lernprozess. Viele Teile sind noch experimentell und werden Schritt für Schritt verbessert.

## Aktueller Stand

meleonAI ist aktuell ein funktionierender lokaler Prototyp. Der Grundworkflow läuft: Bild laden, analysieren, strukturierte JSON-Daten erzeugen, Textänderungen vorbereiten und das Ergebnis im Workflow anzeigen.

Es ist noch kein fertiges Produkt, aber die Kernidee funktioniert.

Was bereits vorhanden ist:

* Oberfläche mit mehreren Screens
* Bildauswahl und Vorschau
* Quick-Actions für typische Bildaufgaben
* OpenAI-Anbindung
* Scout-Analyse mit JSON-Ausgabe
* Artist-Phase für Textanpassung
* Zusammenführen von Analyse- und Änderungsdaten
* Vorher/Nachher-Beispiele für die Portfolio-Seite

Was noch ausgebaut werden soll:

* Mehr auswählbare Zielsprachen
* Bessere Bedienung im Pro-Modus
* Export-Optionen für fertige Ergebnisse
* Batch-Verarbeitung für mehrere Bilder
* Mehr Kontrolle über Stil, Zielgruppe und Textlänge
* Spätere Web-App-Version
* Eventuell Video- oder Diashow-Unterstützung

## Roadmap

Der aktuelle lokale Workflow läuft bereits stabil. Als Nächstes möchte ich das Projekt eher ausbauen als reparieren.

Geplant sind vor allem mehr Bedienkomfort, bessere Exportmöglichkeiten und mehr Kontrolle über die Verarbeitung. Langfristig wäre eine Web-App interessant, damit der Workflow nicht nur lokal nutzbar ist.

## Was ich gelernt habe

Das Projekt war für mich ein Einstieg in Python außerhalb kleiner Übungsaufgaben. Besonders spannend waren die Arbeit mit Dateien, API-Requests, JSON-Daten und die Frage, wie man KI-Ausgaben so strukturiert, dass ein Programm damit weiterarbeiten kann.

Ich habe gelernt, dass „KI ins Programm einbauen“ nicht automatisch bedeutet, dass alles einfacher wird. Der schwierige Teil ist oft nicht der API-Call selbst, sondern alles drumherum: gute Eingaben bauen, Ausgaben prüfen, Fehlerfälle abfangen und die einzelnen Schritte sauber voneinander trennen.

Gerade durch die vielen fehlgeschlagenen Prompts, API-Unterschiede und Umwege habe ich viel mehr gelernt, als wenn es direkt beim ersten Versuch funktioniert hätte.
