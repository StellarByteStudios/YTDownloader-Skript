import yt_dlp
import os
import sys
import spotdl as spotdl_lib
from spotdl.utils.config import DEFAULT_CONFIG


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
    spotdl = spotdl_lib.Spotdl(
        client_id=DEFAULT_CONFIG["client_id"],
        client_secret=DEFAULT_CONFIG["client_secret"],
        downloader_settings={
            "output": os.path.join(target_folder, "{title} - {artist}.{output-ext}"),
            "format": "mp3",
        },
    )
 
    try:
        print(f"\n--- Suche Songs der Spotify-Playlist ---")
        songs = spotdl.search([url])
        print(f"{len(songs)} Song(s) gefunden. Starte Download in: {target_folder}\n")
 
        results = spotdl.download_songs(songs)
 
        erfolgreich = sum(1 for song, path in results if path is not None)
        print(f"\nFertig! {erfolgreich}/{len(songs)} Songs erfolgreich heruntergeladen.")
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
