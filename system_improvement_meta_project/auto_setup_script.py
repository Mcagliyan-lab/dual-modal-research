import json
import os
import shutil
import datetime
import re

def collect_project_info():
    """
    Kullanıcıdan yeni proje için temel bilgileri toplar.
    """
    print("--- Yeni Proje Kurulum Bilgileri ---")
    project_info = {}

    project_info["PROJE_ADI"] = input("Proje Adı: ")
    project_info["KRITIK_ODAK_ALANI"] = input("Kritik Odak Alanı: ")

    # Dosya yolları için varsayılan değerler ve özelleştirme
    project_info["PROJE_ANALIZ_RAPORU_DOSYASI"] = input(f"Proje Analiz Raporu Dosya Yolu (Varsayılan: project_docs/proje_analiz_raporu.md): ") or "project_docs/proje_analiz_raporu.md"
    project_info["PROJE_CALISMA_PLANI_DOSYASI"] = input(f"Proje Çalışma Planı Dosya Yolu (Varsayılan: project_docs/proje_calisma_plani.md): ") or "project_docs/proje_calisma_plani.md"
    project_info["AI_OTURUM_NOTLARI_DOSYASI"] = input(f"AI Oturum Notları Dosya Yolu (Varsayılan: project_docs/ai_session_notes.md): ") or "project_docs/ai_session_notes.md"
    project_info["PROBLEM_COZUM_LOG_DOSYASI"] = input(f"Problem Çözüm Kaydı Dosya Yolu (Varsayılan: project_docs/problem_solution_log.md): ") or "project_docs/problem_solution_log.md"
    project_info["AI_TODO_LIST_DOSYASI"] = input(f"AI Yapılacaklar Listesi Dosya Yolu (Varsayılan: project_docs/ai_todo_list.md): ") or "project_docs/ai_todo_list.md"
    project_info["TASK_PROGRESS_DOSYASI"] = input(f"Görev İlerleme Dosya Yolu (Varsayılan: project_docs/task_progress.md): ") or "project_docs/task_progress.md"
    project_info["UYARI_RAPORU_DOSYASI"] = input(f"Uyarı Raporu Dosya Yolu (Varsayılan: project_docs/uyari_raporu.md): ") or "project_docs/uyari_raporu.md"

    project_info["ILK_CALISMA_PLANI_FAZI_BASLIGI"] = input("İlk Çalışma Planı Faz Başlığı (Örn: Başlangıç ve Planlama): ")
    project_info["GUNCEL_PROJE_DURUMU"] = "Başlatıldı" # Varsayılan değer
    project_info["OTURUM_TARIHI"] = input(f"Oturum Tarihi (YYYY-MM-DD, Varsayılan: {datetime.date.today().isoformat()}): ") or datetime.date.today().isoformat()

    # Diğer alanlar boş bırakılabilir veya varsayılan değerler atanabilir
    project_info["OTURUM_BASARI_OZETI"] = ""
    project_info["KANIT_KALITESI"] = ""
    project_info["YAYIN_HAZIRLIGI"] = ""
    project_info["YENI_ODAK"] = ""
    project_info["GUNCEL_FAZ"] = ""
    project_info["ONERILEN_YOL"] = ""
    project_info["RISK_SEVIYESI"] = ""
    project_info["ZAMAN_CIZELGESI"] = ""
    project_info["GÜVEN"] = ""
    project_info["GUNCEL_PROJE_DURUMU_INGILIZCE"] = ""
    project_info["BIR_SONRAKI_DONUM_NOKTASI"] = ""
    project_info["RISK_SEVIYESI_SON"] = ""
    project_info["ACIL_EYLEM_GEREKLILIGI"] = ""
    project_info["SON_GUNCELLEME_TARIHI"] = ""
    project_info["BIR_SONRAKI_INCELEME"] = ""

    return project_info

def collect_predefined_project_info():
    """
    Yeni proje için önceden tanımlanmış bilgileri döndürür (otomatik çalıştırma için).
    """
    today = datetime.date.today().isoformat()
    project_info = {
        "PROJE_ADI": "Örnek Yeni Proje",
        "KRITIK_ODAK_ALANI": "Web Uygulaması Geliştirme",
        "PROJE_ANALIZ_RAPORU_DOSYASI": "project_docs/proje_analiz_raporu.md",
        "PROJE_CALISMA_PLANI_DOSYASI": "project_docs/proje_calisma_plani.md",
        "AI_OTURUM_NOTLARI_DOSYASI": "project_docs/ai_session_notes.md",
        "PROBLEM_COZUM_LOG_DOSYASI": "project_docs/problem_solution_log.md",
        "AI_TODO_LIST_DOSYASI": "project_docs/ai_todo_list.md",
        "TASK_PROGRESS_DOSYASI": "project_docs/task_progress.md",
        "UYARI_RAPORU_DOSYASI": "project_docs/uyari_raporu.md",
        "ILK_CALISMA_PLANI_FAZI_BASLIGI": "Gereksinim Analizi ve Planlama",
        "GUNCEL_PROJE_DURUMU": "Başlatıldı",
        "OTURUM_TARIHI": today,
        "OTURUM_BASARI_OZETI": "",
        "KANIT_KALITESI": "",
        "YAYIN_HAZIRLIGI": "",
        "YENI_ODAK": "",
        "GUNCEL_FAZ": "",
        "ONERILEN_YOL": "",
        "RISK_SEVIYESI": "",
        "ZAMAN_CIZELGESI": "",
        "GÜVEN": "",
        "GUNCEL_PROJE_DURUMU_INGILIZCE": "",
        "BIR_SONRAKI_DONUM_NOKTASI": "",
        "RISK_SEVIYESI_SON": "",
        "ACIL_EYLEM_GEREKLILIGI": "",
        "SON_GUNCELLEME_TARIHI": "",
        "BIR_SONRAKI_INCELEME": ""
    }
    return project_info

def create_project_config(project_info, config_path="project_config.json"):
    """
    Toplanan proje bilgilerini project_config.json dosyasına yazar.
    """
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(project_info, f, indent=2, ensure_ascii=False)
    print(f"{config_path} başarıyla oluşturuldu.")

def update_project_config(updates, config_path="project_config.json"):
    """
    project_config.json dosyasını verilen güncellemelerle günceller.
    """
    if not os.path.exists(config_path):
        print(f"Hata: {config_path} bulunamadı. Güncelleme yapılamıyor.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config.update(updates)

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"{config_path} başarıyla güncellendi.")

def extract_tasks_from_plan(plan_file_path):
    """
    Proje Çalışma Planı dosyasından görev bilgilerini çıkarır.
    """
    if not os.path.exists(plan_file_path):
        print(f"Hata: {plan_file_path} bulunamadı. Görevler çıkarılamıyor.")
        return []

    tasks = []
    with open(plan_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Görev bloklarını yakalayan regex
    # Her bir görev '-\s\*\*ID:\*\*\s*(\d+)' ile başlar ve bir sonraki görev başlangıcına veya dosya sonuna kadar devam eder.
    task_blocks = re.findall(r'- \*\*ID:\*\*\s*(\d+)(.*?)(?=(?:- \*\*ID:\*\*\s*\d+)|$)', content, re.DOTALL)

    for task_id, block_content in task_blocks:
        task = {"ID": task_id}

        # Her bir alan için regex
        fields = {
            "Ad": r'\*\*Ad:\*\*\s*(.*)',
            "Açıklama": r'\*\*Açıklama:\*\*\s*(.*)',
            "Durum": r'\*\*Durum:\*\*\s*(.*)',
            "İlerleme": r'\*\*İlerleme:\*\*\s*(.*)',
            "Yapılacaklar": r'\*\*Yapılacaklar:\*\*\s*\n(?P<todos>(?:\s*-\s*.*\n)*)',
            "Notlar": r'\*\*Notlar:\*\*\s*(.*)',
            "Son Güncelleme": r'\*\*Son Güncelleme:\*\*\s*(.*)'
        }

        for field_name, pattern in fields.items():
            match = re.search(pattern, block_content)
            if match:
                if field_name == "Yapılacaklar":
                    # Yapılacaklar listesini satır satır ayır ve temizle
                    todos_raw = match.group("todos").strip()
                    task[field_name] = [todo.strip().lstrip('-').strip() for todo in todos_raw.split('\n') if todo.strip()]
                else:
                    task[field_name] = match.group(1).strip()
            else:
                task[field_name] = ""
        tasks.append(task)

    return tasks

def update_task_in_plan(plan_file_path, task_id, updates):
    """
    Proje Çalışma Planı dosyasındaki belirli bir görevin alanlarını günceller.
    
    Args:
        plan_file_path (str): Çalışma planı dosyasının yolu
        task_id (str): Güncellenecek görevin ID'si
        updates (dict): Güncellenecek alanlar ve yeni değerleri
    """
    if not os.path.exists(plan_file_path):
        print(f"Hata: {plan_file_path} bulunamadı. Görev güncellenemiyor.")
        return

    with open(plan_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Belirli görevin bloğunu bul
    pattern = rf'(- \*\*ID:\*\*\s*{re.escape(task_id)})(.*?)(?=(?:- \*\*ID:\*\*\s*\d+\.\d+)|$)'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print(f"Görev ID {task_id} bulunamadı.")
        return

    task_block = match.group(0)
    updated_block = task_block

    # Her bir güncelleme için
    for field_name, new_value in updates.items():
        field_patterns = {
            "Durum": r'(\*\*Durum:\*\*\s*)(.*?)(\n)',
            "İlerleme": r'(\*\*İlerleme:\*\*\s*)(.*?)(\n)',
            "Açıklama": r'(\*\*Açıklama:\*\*\s*)(.*?)(\n)',
            "Notlar": r'(\*\*Notlar:\*\*\s*)(.*?)(\n)',
            "Son Güncelleme": r'(\*\*Son Güncelleme:\*\*\s*)(.*?)(\n)'
        }
        
        if field_name in field_patterns:
            pattern = field_patterns[field_name]
            replacement = rf'\g<1>{new_value}\g<3>'
            updated_block = re.sub(pattern, replacement, updated_block)

    # Orijinal içerikte görev bloğunu güncelle
    updated_content = content.replace(task_block, updated_block)

    # Dosyayı güncelle
    with open(plan_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"Görev {task_id} başarıyla güncellendi.")

def update_config_from_session_notes(session_notes_path, config_path="project_config.json"):
    """
    AI oturum notlarından bilgi çekerek project_config.json dosyasını günceller.
    """
    if not os.path.exists(session_notes_path):
        print(f"Hata: {session_notes_path} bulunamadı. Oturum notlarından güncelleme yapılamıyor.")
        return

    updates = {}
    with open(session_notes_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Yeni Odak Alani
    match_yeni_odak = re.findall(r'^\+\s*\*\*Yeni Odak:\*\*\s*(.*)', content, re.MULTILINE)
    if match_yeni_odak:
        updates["YENI_ODAK"] = match_yeni_odak[-1].strip()

    # Guncel Proje Durumu (Turkce)
    match_guncel_durum = re.findall(r'^\+\s*\*\*Durum:\*\*\s*(.*)', content, re.MULTILINE)
    if match_guncel_durum:
        status_text = match_guncel_durum[-1].strip()
        updates["GUNCEL_PROJE_DURUMU"] = status_text.replace('✅', '').replace('🚀', '')

    # Guncel Proje Durumu (Ingilizce)
    match_current_status_en = re.findall(r'CURRENT STATUS:\s*([\w\s]+)', content, re.MULTILINE)
    if match_current_status_en:
        updates["GUNCEL_PROJE_DURUMU_INGILIZCE"] = match_current_status_en[-1].strip()

    # Bir Sonraki Dönüm Noktası
    match_next_milestone = re.findall(r'^\+\s*\*\*Bir Sonraki Büyük Dönüm Noktası:\*\*\s*(.*)', content, re.MULTILINE)
    if match_next_milestone:
        updates["BIR_SONRAKI_DONUM_NOKTASI"] = match_next_milestone[-1].strip()

    # Risk Seviyesi (son)
    match_risk_level_son = re.findall(r'^\+\s*\*\*Risk Seviyesi:\*\*\s*(.*?)(?:\n|$)', content, re.MULTILINE)
    if match_risk_level_son:
        updates["RISK_SEVIYESI_SON"] = match_risk_level_son[-1].strip()

    # Acil Eylem Gerekliligi
    match_urgent_action = re.findall(r'^\+\s*\*\*Acil Eylem Gerekliliği:\*\*\s*(.*)', content, re.MULTILINE)
    if match_urgent_action:
        updates["ACIL_EYLEM_GEREKLILIGI"] = match_urgent_action[-1].strip()

    # Son Guncelleme Tarihi
    match_last_update_date = re.findall(r'^\+\s*Son Güncelleme:\*\*\s*(.*)', content, re.MULTILINE)
    if match_last_update_date:
        updates["SON_GUNCELLEME_TARIHI"] = match_last_update_date[-1].strip()

    # Bir Sonraki İnceleme
    match_next_review = re.findall(r'^\+\s*\*\*Bir Sonraki İnceleme:\*\*\s*(.*)', content, re.MULTILINE)
    if match_next_review:
        updates["BIR_SONRAKI_INCELEME"] = match_next_review[-1].strip()

    if updates:
        print("Oturum notlarından aşağıdaki güncellemeler tespit edildi:")
        for key, value in updates.items():
            print(f"  {key}: {value}")
        update_project_config(updates, config_path)
    else:
        print("Oturum notlarından güncellenecek herhangi bir bilgi bulunamadı.")

def process_templates(project_info, templates_dir="templates", target_docs_dir="project_docs"):
    """
    Şablon dosyalarını kopyalar ve içlerindeki yer tutucuları doldurur.
    """
    os.makedirs(target_docs_dir, exist_ok=True)

    template_map = {
        "generic_ai_project_manager_prompt_template.md": "ai_project_manager_prompt.md",
        "problem_solution_log_template.md": "problem_solution_log.md",
        "ai_session_notes_template.md": "ai_session_notes.md",
        "proje_analiz_raporu_template.md": "proje_analiz_raporu.md",
        "proje_calisma_plani_template.md": "proje_calisma_plani.md",
        "ai_todo_list_template.md": "ai_todo_list.md",
        "task_progress_template.md": "task_progress.md",
        "uyari_raporu_template.md": "uyari_raporu.md"
    }

    print(f"\nŞablonlar \'{templates_dir}\' dizininden \'{target_docs_dir}\' dizinine kopyalanıyor ve yer tutucular dolduruluyor...")

    for template_filename, target_filename in template_map.items():
        template_path = os.path.join(templates_dir, template_filename)
        target_path = os.path.join(target_docs_dir, target_filename)

        if not os.path.exists(template_path):
            print(f"Uyarı: \'{template_path}\' bulunamadı. Kopyalama atlanıyor.")
            continue

        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Yer tutucuları doldur
        for key, value in project_info.items():
            # replace için özel durum: bazı yer tutucular dosya yolu içinde
            # bu yüzden PROJE_ADI ve KRITIK_ODAK_ALANI gibi doğrudan metin
            # olanlar için de replace yaparız.
            content = content.replace(f"[{key}]", str(value))

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"\'{target_filename}\' başarıyla oluşturuldu ve yer tutucuları dolduruldu.")

    print("\nTüm şablon dosyaları başarıyla işlendi.")

if __name__ == "__main__":
    # Örnek proje için yeni bir dizin oluştur
    new_project_root = "new_example_project"
    os.makedirs(new_project_root, exist_ok=True)

    # Çalışma dizinini geçici olarak yeni proje dizinine taşı
    original_cwd = os.getcwd()
    os.chdir(new_project_root)

    try:
        # Önceden tanımlanmış bilgileri topla
        info = collect_predefined_project_info()
        
        # project_config.json'ı oluştur
        create_project_config(info)
        
        # Şablonları kopyala ve doldur
        # templates dizininin ana dizinde olduğunu varsayıyoruz
        process_templates(info, templates_dir=os.path.join(original_cwd, "templates"))

        print("\nOtomatik kurulum scripti tamamlandı: Yeni proje belgeleri oluşturuldu ve yer tutucular dolduruldu.")
    finally:
        # Orijinal çalışma dizinine geri dön
        os.chdir(original_cwd) 