import os
import sys

# auto_setup_script.py dosyasını import edebilmek için yolu sys.path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auto_setup_script

# Meta-projenin kendi dosyalarına giden yollar
META_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN_FILE = os.path.join(META_PROJECT_ROOT, "proje_calisma_plani.md")

if __name__ == "__main__":
    print(f"'{PLAN_FILE}' dosyasından görevler çıkarılıyor...")
    tasks = auto_setup_script.extract_tasks_from_plan(PLAN_FILE)

    if tasks:
        print("Çıkarılan Görevler:")
        for task in tasks:
            print(f"  ID: {task.get('ID')}")
            print(f"  Ad: {task.get('Ad')}")
            print(f"  Durum: {task.get('Durum')}")
            print(f"  İlerleme: {task.get('İlerleme')}")
            print(f"  Açıklama: {task.get('Açıklama')}")
            print(f"  Notlar: {task.get('Notlar')}")
            print(f"  Son Güncelleme: {task.get('Son Güncelleme')}")
            print("  Yapılacaklar:")
            if task.get('Yapılacaklar'):
                for todo in task['Yapılacaklar']:
                    print(f"    - {todo}")
            else:
                print("    (Yok)")
            print("-" * 30)
    else:
        print("Görev bulunamadı veya bir hata oluştu.") 