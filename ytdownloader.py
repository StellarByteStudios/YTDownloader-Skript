import yt_dlp
import os
import sys


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

if __name__ == "__main__":
    # Falls die Batch einen Pfad übergibt, nimm diesen, sonst das Skript-Verzeichnis
    if len(sys.argv) > 1:
        start_dir = sys.argv[1]
    else:
        start_dir = os.getcwd()
    
    print(f"--- YouTube Downloader ---")
    print(f"Aktueller Pfad: {start_dir}\n")
    
    link = input("YouTube-Link: ").strip()
    
    # Nutzer fragen, ob er den Pfad ändern will, sonst einfach Enter
    folder_input = input(f"Zielordner (Enter für aktuellen Ordner): ").strip()
    
    # Wenn keine Eingabe erfolgt, nimm den aktuellen Ordner
    if folder_input:
        target = os.path.join(start_dir, folder_input)
    else:
        target = start_dir

    if link:
        download_youtube_audio(link, target)
    else:
        print("Abgebrochen: Kein Link vorhanden.")