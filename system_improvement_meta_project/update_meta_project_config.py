import os
import sys
import json
import re

# auto_setup_script.py dosyasını import edebilmek için yolu sys.path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auto_setup_script

# Meta-projenin kendi dosyalarına giden yollar
META_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(META_PROJECT_ROOT, "project_config.json")
SESSION_NOTES_FILE = os.path.join(META_PROJECT_ROOT, "ai_session_notes.md")

if __name__ == "__main__":
    print("Meta-projenin project_config.json dosyasını, ai_session_notes.md'den alınan bilgilerle güncelleme işlemi başlatılıyor...")
    auto_setup_script.update_config_from_session_notes(SESSION_NOTES_FILE, CONFIG_FILE)
    print("Güncelleme işlemi tamamlandı.") 