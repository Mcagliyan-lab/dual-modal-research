import os
import sys
import datetime

# auto_setup_script.py dosyasını import edebilmek için yolu sys.path'e ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import auto_setup_script

# Meta-projenin kendi dosyalarına giden yollar
META_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PLAN_FILE = os.path.join(META_PROJECT_ROOT, "proje_calisma_plani.md")

if __name__ == "__main__":
    print(f"Görev 1.2'nin durumu güncelleniyor...")
    
    # Görev 1.2'yi güncelle: Durum: Tamamlandı, İlerleme: 100%, Son Güncelleme: bugünün tarihi
    updates = {
        "Durum": "Tamamlandı", 
        "İlerleme": "100%",
        "Son Güncelleme": datetime.date.today().isoformat()
    }
    
    auto_setup_script.update_task_in_plan(PLAN_FILE, "1.2", updates)
    
    print("Görev 1.2 güncelleme işlemi tamamlandı.")
    
    # Güncellenen görevleri tekrar oku ve doğrula
    print("\nGüncellenmiş görevler kontrol ediliyor...")
    tasks = auto_setup_script.extract_tasks_from_plan(PLAN_FILE)
    
    # ID=1 olan ikinci görevi bul (1.2)
    task_1_2 = None
    task_1_count = 0
    for task in tasks:
        if task.get('ID') == '1':
            task_1_count += 1
            if task_1_count == 2:  # İkinci ID=1 görev (1.2)
                task_1_2 = task
                break
    
    if task_1_2:
        print(f"Görev 1.2 güncel durumu:")
        print(f"  Ad: {task_1_2.get('Ad')}")
        print(f"  Durum: {task_1_2.get('Durum')}")
        print(f"  İlerleme: {task_1_2.get('İlerleme')}")
        print(f"  Son Güncelleme: {task_1_2.get('Son Güncelleme')}")
    else:
        print("Görev 1.2 bulunamadı.") 