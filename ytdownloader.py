import yt_dlp
import os
import sys
import time
import spotdl as spotdl_lib
from spotdl.utils.config import DEFAULT_CONFIG

MAX_RETRIES = 3        # Wie oft ein fehlgeschlagener Song erneut versucht wird
RETRY_DELAY = 5         # Wartezeit in Sekunden zwischen den Versuchen



def download_youtube_audio(url, target_folder):
    # Sicherstellen, dass der Ordner existiert
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Ordner '{target_folder}' wurde erstellt.")

    # Pfad-Vorlage erstellen: Ordner + Dateiname
    # '%(title)s.%(ext)s' ist der Platzhalter für den Youtube-Titel
    output_path = os.path.join(target_folder, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path, # Hier wird der Zielordner gesetzt
        'noplaylist': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"\n--- Starte Download in: {target_folder} ---")
            ydl.download([url])
            print("\nFertig! Alle Dateien liegen bereit.")
    except Exception as e:
        print(f"Hoppla, da lief was schief: {e}")








def download_spotify_playlist(url, target_folder):
    """
    Nutzt spotdl: holt Metadaten von Spotify (Titel, Künstler),
    sucht den passenden Track auf YouTube und lädt ihn als MP3 herunter.
    """
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"Ordner '{target_folder}' wurde erstellt.")
 
    # Spotify-App-Zugangsdaten (Client-ID/Secret) werden von spotdl
    # standardmäßig mitgeliefert. Falls das nicht funktioniert, siehe
    # Hinweis am Ende der Datei zum Erstellen eigener Zugangsdaten.
    client = spotdl_lib.Spotdl(
        client_id=DEFAULT_CONFIG["client_id"],
        client_secret=DEFAULT_CONFIG["client_secret"],
        downloader_settings={
            # "output": os.path.join(target_folder, "{title} - {artist}.{output-ext}"),
            "output": os.path.join(target_folder, "{artist}", "{album} ({year})", "{track-number} - {title} - {artist}.{output-ext}"),
            "format": "mp3",
        },
    )
 
    try:
        print(f"\n--- Suche Songs der Spotify-Playlist ---")
 
        # Versuche die Metadaten von Spotify zu crawlen
        songs = []
        for versuch in range(1, MAX_RETRIES + 1):
            try:
                songs = client.search([url])
                break
            except Exception as e:
                print(f"Suche fehlgeschlagen (Versuch {versuch}/{MAX_RETRIES}): {e}")
                if versuch < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                else:
                    raise
 
        # Alle Metadaten zusammen
        print(f"{len(songs)} Song(s) gefunden. Starte Download in: {target_folder}\n")
 


        # Songs von YT Downloaden
        results = client.download_songs(songs)
 



        # Fehlgeschlagene Songs sammeln und erneut versuchen
        erfolgreich_ergebnisse = [(s, p) for s, p in results if p is not None]
        fehlgeschlagen = [s for s, p in results if p is None]
 

        # Fehlerhafte Downloads nochmal neu probieren
        versuch = 1
        while (len(fehlgeschlagen) > 0) and (versuch <= MAX_RETRIES):
            print(f"\n{len(fehlgeschlagen)} Song(s) fehlgeschlagen. "
                  f"Erneuter Versuch {versuch}/{MAX_RETRIES} in {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)
 
            noch_fehlgeschlagen = []
            for song in fehlgeschlagen:
                try:
                    _, pfad = client.download(song)
                    if pfad is not None:
                        erfolgreich_ergebnisse.append((song, pfad))
                    else:
                        noch_fehlgeschlagen.append(song)
                except Exception as e:
                    print(f"  Weiterhin fehlgeschlagen: {song.display_name} - {e}")
                    noch_fehlgeschlagen.append(song)
 
            fehlgeschlagen = noch_fehlgeschlagen
            versuch += 1
 
        results = erfolgreich_ergebnisse
 
        erfolgreich = len(results)
        print(f"\nFertig! {erfolgreich}/{len(songs)} Songs erfolgreich heruntergeladen.")
 

        if fehlgeschlagen:
            print(f"Endgültig fehlgeschlagen ({len(fehlgeschlagen)}):")
            for song in fehlgeschlagen:
                print(f"  - {song.display_name}")


    except Exception as e:
        print(f"Hoppla, da lief was schief: {e}")
 
 






def erkenne_plattform(url):
    """Erkennt anhand der URL, ob es sich um Spotify oder YouTube handelt."""
    if "spotify.com" in url:
        return "spotify"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    else:
        return None










if __name__ == "__main__":
    # Falls die Batch einen Pfad übergibt, nimm diesen, sonst das Skript-Verzeichnis
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        start_dir = os.getcwd()


    # So lange True, wie noch Zeug heruntergeladen werden soll
    extra_round = True
 

    while extra_round:

        extra_round = False

        print(f"--- YouTube / Spotify Downloader ---")
        print(f"Aktueller Pfad: {start_dir}\n")
    
        link = input("YouTube- oder Spotify-Link: ").strip()
    
        # Nutzer fragen, ob er den Pfad ändern will, sonst einfach Enter
        folder_input = input(f"Zielordner (Enter für aktuellen Ordner): ").strip()
    
        # Wenn keine Eingabe erfolgt, nimm den aktuellen Ordner
        if folder_input:
            target = os.path.join(start_dir, folder_input)
        else:
            target = start_dir
    
        if not link:
            print("Abgebrochen: Kein Link vorhanden.")
            sys.exit(0)
    
        plattform = erkenne_plattform(link)
    
        if plattform == "youtube":
            download_youtube_audio(link, target)
        elif plattform == "spotify":
            download_spotify_playlist(link, target)
        else:
            print("Abgebrochen: Der Link wurde weder als YouTube- noch als Spotify-Link erkannt.")


        """ Funktioniert noch nicht
        # Weitermachen?
        another_download = input(f"Nochwas herunterladen? [y, j, ja, yes]").strip().lower()

        # Set an möglichen antworten
        yesses = {"y", "yes", "j", "ja"}
        if another_download in yesses:
            extra_round = True
        """
        
