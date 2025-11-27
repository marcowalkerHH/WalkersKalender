# Walkers Christmas Calendar

Interaktive Ein-Seiten-Anwendung als Adventskalender für Noah, Johanna und Sibylle. Der Kalender läuft komplett im Browser, speichert den Fortschritt lokal und funktioniert auf iPad, iPhone und Desktop.

## Features
- Herzintro, Matrix-Übergang und anschließender Login mit Sicherheitsfrage.
- Individuell gestaltete Kalender-Ansichten je Familienmitglied inklusive animiertem Schneefall.
- Zwei Modi (Offen & Advent). Der Advent-Modus erlaubt nur Türchen bis zum aktuellen Datum und kann ausschließlich mit Admin-Code gewechselt werden.
- Fragenpools pro Person (normal & schwer) aus JSON-Dateien, ausgewogene Kategorienlogik, erneutes Mischen per Button.
- Punkte- & Level-System, Kronen-Overlay ab 50 Punkten, jederzeit sichtbare Score-Leiste.
- Adminbereich zum Zurücksetzen aller Punkte sowie zum Moduswechsel, geschützt per Geheimcode (in `app.js` als `ADMIN_CODE` hinterlegt).
- Optionaler Hintergrundmusik-Player mit Playlist, Musik-/Lautstärketoggle sowie Track-Skip. Einstellungen persistieren via `localStorage`.

## Entwicklung & Nutzung
1. Projekt klonen und in das Verzeichnis wechseln.
2. Mit einem beliebigen statischen Server starten, z. B. `npx serve` oder `python -m http.server`.
3. `index.html` im Browser öffnen. Die Anwendung verwaltet sämtliche Daten rein clientseitig.

### Fragen erweitern
- JSON-Dateien liegen in `questions/`. Jede Frage besitzt `category`, `question`, `answers`, `correctIndex` und `difficulty` (`normal` oder `hard`).
- Zusätzliche Fragen einfach anhängen. Die Auswahl priorisiert weniger verwendete Kategorien automatisch.
- Die Datei `scripts/generate_questions.py` erzeugt die JSON-Dateien aus gepflegten Faktensammlungen. Nach Anpassungen genügt `python scripts/generate_questions.py`, um alle Dateien konsistent mit exakt 30 Fragen pro Kategorie neu zu generieren.

### Audio anpassen
- Um Pull-Requests ohne Binärdateien zu ermöglichen, enthält das Repo keine Audiodateien.
- Lege eigene, lizenzfreie MP3s im Ordner `assets/audio/` (oder einem beliebigen Pfad) ab.
- Definiere vor dem Laden von `app.js` ein Playlist-Array, z. B. in `index.html`:

  ```html
  <script>
    window.WALKERS_AUDIO_TRACKS = [
      'assets/audio/dein-track-1.mp3',
      'assets/audio/dein-track-2.mp3'
    ];
  </script>
  <script src="app.js"></script>
  ```

- Ohne diese Definition bleiben die Musik-Controls deaktiviert.

### Fehlerbehebung
- **Intro bleibt stehen oder UI lädt nicht vollständig?** Seit diesem Update fängt die App fehlende DOM-Elemente und defekte `localStorage`-Einträge automatisch ab. Sollte dennoch etwas hängen bleiben, Browser-Tab einmal neu laden oder den lokalen Speicher der Seite löschen.
- **Verbogene Punktestände/Kategorien?** Über den Adminbereich (Code steht in `app.js` als `ADMIN_CODE`) lassen sich Punkte zurücksetzen sowie Fragen neu mischen.
- **Konsole meldet fehlende JSON-Dateien?** Sicherstellen, dass der Server die Dateien aus `questions/` ausliefert (bei reinem `file://`-Aufruf werden Fetches vom Browser blockiert – daher bitte immer über einen kleinen Dev-Server arbeiten).

## Lizenz
Privates Familienprojekt. Weitere Nutzung auf eigene Verantwortung.

## Ideen für weitere Verbesserungen
- **Mini-Games in den Türchen**: Statt nur Fragen könnten einzelne Tage kleine Spielereien bieten (Memory, Schiebepuzzle, Wortsuche), die auf den jeweiligen Stil der Person angepasst sind.
- **Tägliche Erfolge**: Ergänze Achievements wie „3 richtige Antworten am Stück“ oder „Alle Türen der Woche geöffnet“ und zeige sie als Sticker unter der Scoreleiste.
- **Geteilte Momente**: Erlaube das Exportieren eines Türchen-Screenshots inklusive Punktestand, damit die Familie Highlights teilen kann.
- **Audiovisuelle Abwechslung**: Hinterlege pro Person eigene kurze Jingles für richtige Antworten oder Level-Ups, die über das bestehende Musik-Setup eingebunden werden können.
- **Barrierefreiheit**: Ergänze Tastatursteuerung, größere Kontraste und optionale Sprachausgabe der Fragen, damit auch bei hellem Licht oder für Kinder das Lesen leichter fällt.
- **Progressives Web App (PWA)**: Mit einem Manifest und einem Service Worker könnte der Kalender offline verfügbar und installierbar werden.
