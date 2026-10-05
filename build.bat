@echo off
echo Building Fish Catching Game...
pyinstaller --name "fish" --noconfirm --onefile --windowed --add-data "background.png;." --add-data "error.png;." --add-data "bucket.png;." --add-data "fish.png;." --add-data "music.mp3;." --add-data "vocals.mp3;." main.py
echo Build complete! The executable is located in the "dist" folder.
pause
