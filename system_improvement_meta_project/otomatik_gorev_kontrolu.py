#!/usr/bin/env python3
"""
Otomatik Görev Kontrol Scripti
==============================

Bu script, proje görevlerinin kod tabanı ve diğer belgeler arasındaki tutarlılığını analiz eder
ve uyarı raporu oluşturur.

Kullanım:
    python otomatik_gorev_kontrolu.py [--config config.json] [--output uyari_raporu.md]
"""

import json
import os
import argparse
import re
import datetime
from pathlib import Path
from typing import List, Dict, Any

class TaskConsistencyChecker:
    def __init__(self, config_path: str = "project_config.json"):
        """Görev tutarlılık kontrol sınıfını başlatır."""
        self.config_path = config_path
        self.config = self.load_config()
        self.warnings = []
        self.statistics = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "in_progress_tasks": 0,
            "not_started_tasks": 0,
            "inconsistencies": 0
        }

    def load_config(self) -> Dict[str, Any]:
        """Proje yapılandırma dosyasını yükler."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Uyarı: {self.config_path} bulunamadı. Varsayılan değerler kullanılıyor.")
            return {
                "PROJE_CALISMA_PLANI_DOSYASI": "project_docs/proje_calisma_plani.md",
                "AI_TODO_LIST_DOSYASI": "project_docs/ai_todo_list.md",
                "TASK_PROGRESS_DOSYASI": "project_docs/task_progress.md",
                "UYARI_RAPORU_DOSYASI": "project_docs/uyari_raporu.md"
            }

    def extract_tasks_from_plan(self, plan_file_path: str) -> List[Dict[str, Any]]:
        """Çalışma planından görevleri çıkarır."""
        if not os.path.exists(plan_file_path):
            self.warnings.append(f"Çalışma planı dosyası bulunamadı: {plan_file_path}")
            return []

        tasks = []
        with open(plan_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Görev bloklarını yakala
        task_blocks = re.findall(r'- \*\*ID:\*\*\s*(\d+\.\d+)(.*?)(?=(?:- \*\*ID:\*\*\s*\d+\.\d+)|$)', content, re.DOTALL)

        for task_id, block_content in task_blocks:
            task = {"ID": task_id}

            # Her alan için regex
            fields = {
                "Ad": r'\*\*Ad:\*\*\s*(.*)',
                "Açıklama": r'\*\*Açıklama:\*\*\s*(.*)',
                "Durum": r'\*\*Durum:\*\*\s*(.*)',
                "İlerleme": r'\*\*İlerleme:\*\*\s*(.*)',
                "Notlar": r'\*\*Notlar:\*\*\s*(.*)',
                "Son Güncelleme": r'\*\*Son Güncelleme:\*\*\s*(.*)'
            }

            for field_name, pattern in fields.items():
                match = re.search(pattern, block_content)
                task[field_name] = match.group(1).strip() if match else ""

            tasks.append(task)
            self.statistics["total_tasks"] += 1

            # Durum istatistiklerini güncelle
            durum = task.get("Durum", "").lower()
            if "tamamlandı" in durum or "tamamlanmış" in durum:
                self.statistics["completed_tasks"] += 1
            elif "devam" in durum or "başlatıldı" in durum:
                self.statistics["in_progress_tasks"] += 1
            else:
                self.statistics["not_started_tasks"] += 1

        return tasks

    def check_todo_consistency(self, todo_file_path: str, tasks: List[Dict[str, Any]]) -> None:
        """TODO listesi ile görevler arasındaki tutarlılığı kontrol eder."""
        if not os.path.exists(todo_file_path):
            self.warnings.append(f"TODO listesi dosyası bulunamadı: {todo_file_path}")
            return

        with open(todo_file_path, "r", encoding="utf-8") as f:
            todo_content = f.read()

        # Aktif görevleri kontrol et
        active_tasks = [task for task in tasks if task.get("Durum", "").lower() not in ["tamamlandı", "tamamlanmış"]]
        
        for task in active_tasks:
            task_id = task.get("ID", "")
            task_name = task.get("Ad", "")
            
            # TODO listesinde bu görevin bahsedilip edilmediğini kontrol et
            if task_id not in todo_content and task_name not in todo_content:
                self.warnings.append(f"Aktif görev TODO listesinde bulunamadı: {task_id} - {task_name}")
                self.statistics["inconsistencies"] += 1

    def check_progress_consistency(self, progress_file_path: str, tasks: List[Dict[str, Any]]) -> None:
        """İlerleme tablosu ile görevler arasındaki tutarlılığı kontrol eder."""
        if not os.path.exists(progress_file_path):
            self.warnings.append(f"İlerleme tablosu dosyası bulunamadı: {progress_file_path}")
            return

        with open(progress_file_path, "r", encoding="utf-8") as f:
            progress_content = f.read()

        for task in tasks:
            task_id = task.get("ID", "")
            if task_id and task_id not in progress_content:
                self.warnings.append(f"Görev ilerleme tablosunda bulunamadı: {task_id}")
                self.statistics["inconsistencies"] += 1

    def check_date_consistency(self, tasks: List[Dict[str, Any]]) -> None:
        """Görev tarihlerinin tutarlılığını kontrol eder."""
        today = datetime.date.today()
        
        for task in tasks:
            last_update = task.get("Son Güncelleme", "")
            if last_update:
                try:
                    update_date = datetime.datetime.strptime(last_update, "%Y-%m-%d").date()
                    if update_date > today:
                        self.warnings.append(f"Görev {task.get('ID', '')} gelecek tarihli güncelleme içeriyor: {last_update}")
                        self.statistics["inconsistencies"] += 1
                except ValueError:
                    self.warnings.append(f"Görev {task.get('ID', '')} geçersiz tarih formatı: {last_update}")
                    self.statistics["inconsistencies"] += 1

    def generate_report(self, output_path: str) -> None:
        """Uyarı raporunu oluşturur."""
        report_content = f"""# Otomatik Görev Tutarlılık Raporu

**Rapor Tarihi:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Proje:** {self.config.get('PROJE_ADI', 'Bilinmeyen Proje')}

---

## 📊 İstatistikler

| Metrik | Değer |
|--------|-------|
| Toplam Görev | {self.statistics['total_tasks']} |
| Tamamlanan Görev | {self.statistics['completed_tasks']} |
| Devam Eden Görev | {self.statistics['in_progress_tasks']} |
| Başlatılmamış Görev | {self.statistics['not_started_tasks']} |
| Tespit Edilen Tutarsızlık | {self.statistics['inconsistencies']} |

---

## ⚠️ Tespit Edilen Uyarılar

"""
        if self.warnings:
            for i, warning in enumerate(self.warnings, 1):
                report_content += f"{i}. {warning}\n"
        else:
            report_content += "✅ Herhangi bir tutarsızlık tespit edilmedi.\n"

        report_content += f"""

---

## 📋 Öneriler

### Yüksek Öncelikli
- Tespit edilen tutarsızlıkları giderin
- Eksik görev güncellemelerini tamamlayın
- Tarih formatlarını standartlaştırın

### Orta Öncelikli
- Görev durumlarını düzenli olarak güncelleyin
- TODO listesini aktif görevlerle senkronize edin
- İlerleme tablosunu güncel tutun

### Düşük Öncelikli
- Görev açıklamalarını daha detaylandırın
- Bağımlılık ilişkilerini belirtmeyi düşünün

---

**Bu rapor `otomatik_gorev_kontrolu.py` scripti tarafından otomatik olarak oluşturulmuştur.**
"""

        # Çıktı dizinini oluştur
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"Uyarı raporu oluşturuldu: {output_path}")

    def run_analysis(self) -> None:
        """Ana analiz işlemini çalıştırır."""
        print("Görev tutarlılık analizi başlatılıyor...")
        
        # Görevleri çalışma planından çıkar
        plan_file = self.config.get("PROJE_CALISMA_PLANI_DOSYASI", "")
        if plan_file:
            tasks = self.extract_tasks_from_plan(plan_file)
            print(f"  ✓ {len(tasks)} görev bulundu")
            
            # TODO listesi tutarlılığı
            todo_file = self.config.get("AI_TODO_LIST_DOSYASI", "")
            if todo_file:
                self.check_todo_consistency(todo_file, tasks)
                print(f"  ✓ TODO listesi tutarlılığı kontrol edildi")
            
            # İlerleme tablosu tutarlılığı
            progress_file = self.config.get("TASK_PROGRESS_DOSYASI", "")
            if progress_file:
                self.check_progress_consistency(progress_file, tasks)
                print(f"  ✓ İlerleme tablosu tutarlılığı kontrol edildi")
            
            # Tarih tutarlılığı
            self.check_date_consistency(tasks)
            print(f"  ✓ Tarih tutarlılığı kontrol edildi")
        
        # Rapor oluştur
        output_file = self.config.get("UYARI_RAPORU_DOSYASI", "uyari_raporu.md")
        self.generate_report(output_file)
        
        print(f"Analiz tamamlandı. {len(self.warnings)} uyarı tespit edildi.")

def main():
    """Ana fonksiyon."""
    parser = argparse.ArgumentParser(description="Proje görev tutarlılık kontrolü")
    parser.add_argument("--config", default="project_config.json", 
                        help="Yapılandırma dosyası yolu")
    parser.add_argument("--output", 
                        help="Çıktı raporu dosyası yolu (yapılandırmadan alınır)")
    
    args = parser.parse_args()
    
    checker = TaskConsistencyChecker(args.config)
    
    if args.output:
        checker.config["UYARI_RAPORU_DOSYASI"] = args.output
    
    checker.run_analysis()

if __name__ == "__main__":
    main() 