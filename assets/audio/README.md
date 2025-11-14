# Audio-Playlist

In diesem Ordner werden **keine** Audiodateien versioniert, damit Pull-Requests ohne Binäranhang möglich bleiben. Du kannst jedoch beliebige (lizenzfreie) MP3s hier platzieren und sie anschließend als Playlist einbinden:

1. Speichere deine Dateien, z. B. `assets/audio/song-1.mp3`.
2. Ergänze in `index.html` vor `app.js` folgenden Block:

   ```html
   <script>
     window.WALKERS_AUDIO_TRACKS = [
       'assets/audio/song-1.mp3',
       'assets/audio/song-2.mp3'
     ];
   </script>
   ```

Solange keine Playlist definiert ist, bleiben die Musik-Controls deaktiviert.
