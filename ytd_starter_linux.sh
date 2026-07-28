#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/downloader.venv-linux"
SCRIPT_PATH="$SCRIPT_DIR/ytdownloader.py"

# venv automatisch erstellen, falls sie fehlt
if [ ! -d "$VENV_DIR" ]; then
    echo "Erstelle virtuelle Umgebung für Linux..."
    python3 -m venv "$VENV_DIR"
    "$VENV_DIR/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi


# NEU: Zielordner per Dialog auswählen lassen
start_dir=$(kdialog --getexistingdirectory "$HOME" --title "Zielordner wählen")

# Abbrechen, falls der Dialog geschlossen/abgebrochen wurde
if [ -z "$start_dir" ]; then
    echo "Kein Ordner ausgewählt – Abbruch."
    read -p "Drücke Enter zum Beenden..."
    exit 1
fi

echo "$start_dir"

"$VENV_DIR/bin/python" "$SCRIPT_PATH" "$start_dir"

read -p "Drücke Enter zum Beenden..."