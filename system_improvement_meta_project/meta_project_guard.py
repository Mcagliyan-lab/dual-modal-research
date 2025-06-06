#!/usr/bin/env python3
"""
Meta-Proje Koruma Sistemi (Meta-Project Guard System)

Bu script, meta-proje dosyalarının ana projeye karışmasını önler ve 
dosya organizasyonunu korur. Git hooks ve manuel kontroller için kullanılır.

Özellikler:
1. Kök dizinde meta-proje dosyalarını tespit eder
2. Otomatik olarak doğru dizine taşır  
3. Git commit öncesi kontrol yapar
4. Uyarı raporu oluşturur
5. Ana proje güvenliğini korur

Kullanım:
    python meta_project_guard.py --check          # Sadece kontrol et
    python meta_project_guard.py --fix            # Sorunları düzelt
    python meta_project_guard.py --git-hook       # Git hook modu
    python meta_project_guard.py --report         # Detaylı rapor
"""

import os
import re
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

class MetaProjectGuard:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.meta_project_dir = self.root_dir / "system_improvement_meta_project"
        self.log_dir = self.meta_project_dir / "logs"
        
        # Meta-proje ile ilgili dosya kalıpları
        self.meta_patterns = [
            r".*gorev.*\.py$",           # Görev scripti
            r".*task.*\.py$",            # Task scripti  
            r".*meta.*\.py$",            # Meta scripti
            r".*setup.*\.py$",           # Setup scripti
            r".*check.*\.py$",           # Check scripti
            r".*lint.*\.py$",            # Lint scripti
            r".*update.*\.py$",          # Update scripti
            r"Dockerfile$",              # Docker dosyası
            r"docker-compose\.yml$",     # Docker compose
            r".*_report.*\.md$",         # Rapor dosyası
            r"lint_.*\.md$",             # Lint raporu
        ]
        
        # Ana projeye ait dosyalar (dokunulmaz)
        self.protected_patterns = [
            r"README\.md$",
            r"requirements.*\.txt$",
            r"\.git.*",
            r"LICENSE$",
            r"\.pytest_cache.*",
            r"__pycache__.*",
            r"src/.*",
            r"tests/.*",
            r"docs/.*",
            r"examples/.*",
            r"data/.*",
        ]
        
        self.issues = []
        self.fixes_applied = []
        
    def ensure_directories(self):
        """Gerekli dizinleri oluştur"""
        self.meta_project_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        
    def is_meta_project_file(self, file_path: Path) -> bool:
        """Dosyanın meta-proje ile ilgili olup olmadığını kontrol et"""
        relative_path = file_path.relative_to(self.root_dir)
        
        # Meta-proje dizinindeyse zaten doğru yerde
        if str(relative_path).startswith("system_improvement_meta_project"):
            return False
            
        # Korunan dosyalarsa dokunma
        for pattern in self.protected_patterns:
            if re.match(pattern, str(relative_path)):
                return False
                
        # Meta-proje kalıplarıyla eşleşiyor mu?
        for pattern in self.meta_patterns:
            if re.match(pattern, str(relative_path)):
                return True
                
        return False
        
    def scan_root_directory(self) -> List[Path]:
        """Kök dizini tarayarak meta-proje dosyalarını bul"""
        meta_files = []
        
        for item in self.root_dir.iterdir():
            if item.is_file() and self.is_meta_project_file(item):
                meta_files.append(item)
                self.issues.append({
                    "type": "misplaced_file",
                    "file": str(item.relative_to(self.root_dir)),
                    "message": f"Meta-proje dosyası kök dizinde: {item.name}"
                })
                
        return meta_files
        
    def move_file_to_meta_project(self, file_path: Path) -> bool:
        """Dosyayı meta-proje dizinine taşı"""
        try:
            target_path = self.meta_project_dir / file_path.name
            
            # Hedef dosya zaten varsa yedek al
            if target_path.exists():
                backup_name = f"{target_path.name}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = self.meta_project_dir / backup_name
                target_path.rename(backup_path)
                self.fixes_applied.append(f"Yedek alındı: {backup_name}")
                
            # Dosyayı taşı
            shutil.move(str(file_path), str(target_path))
            self.fixes_applied.append(f"Taşındı: {file_path.name} → system_improvement_meta_project/")
            return True
            
        except Exception as e:
            self.issues.append({
                "type": "move_error",
                "file": str(file_path.relative_to(self.root_dir)),
                "message": f"Taşıma hatası: {str(e)}"
            })
            return False
            
    def check_project_isolation(self) -> Dict:
        """Proje izolasyonunu kontrol et"""
        self.ensure_directories()
        
        # Kök dizini tara
        misplaced_files = self.scan_root_directory()
        
        # Meta-proje dizini varlığını kontrol et
        if not self.meta_project_dir.exists():
            self.issues.append({
                "type": "missing_directory",
                "file": "system_improvement_meta_project/",
                "message": "Meta-proje dizini bulunamadı"
            })
            
        # Log dizini varlığını kontrol et
        if not self.log_dir.exists():
            self.issues.append({
                "type": "missing_directory", 
                "file": "system_improvement_meta_project/logs/",
                "message": "Log dizini bulunamadı"
            })
            
        return {
            "total_issues": len(self.issues),
            "misplaced_files": len(misplaced_files),
            "issues": self.issues,
            "status": "CLEAN" if len(self.issues) == 0 else "ISSUES_FOUND"
        }
        
    def fix_issues(self) -> Dict:
        """Tespit edilen sorunları düzelt"""
        self.ensure_directories()
        
        # Önce kontrol et
        check_result = self.check_project_isolation()
        
        if check_result["misplaced_files"] == 0:
            return {
                "status": "NO_FIXES_NEEDED",
                "message": "Düzeltilecek sorun bulunamadı",
                "fixes_applied": []
            }
            
        # Dosyaları taşı
        misplaced_files = self.scan_root_directory()
        success_count = 0
        
        for file_path in misplaced_files:
            if self.move_file_to_meta_project(file_path):
                success_count += 1
                
        return {
            "status": "FIXES_APPLIED",
            "total_files_moved": success_count,
            "fixes_applied": self.fixes_applied,
            "remaining_issues": len([i for i in self.issues if i["type"] != "misplaced_file"])
        }
        
    def git_hook_check(self) -> bool:
        """Git hook için hızlı kontrol (commit engelleyici)"""
        result = self.check_project_isolation()
        
        if result["misplaced_files"] > 0:
            print("🚨 COMMIT ENGELLENDİ!")
            print(f"Meta-proje dosyaları kök dizinde tespit edildi: {result['misplaced_files']} dosya")
            print("\nÖnce şu komutu çalıştırın:")
            print("python system_improvement_meta_project/meta_project_guard.py --fix")
            return False
            
        return True
        
    def generate_report(self) -> str:
        """Detaylı rapor oluştur"""
        result = self.check_project_isolation()
        
        report = f"""
# Meta-Proje Koruma Raporu

**Tarih:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Durum:** {result['status']}
**Toplam Sorun:** {result['total_issues']}

## 📊 Özet

- ✅ Meta-proje dizini: {'Mevcut' if self.meta_project_dir.exists() else 'Eksik'}
- ✅ Log dizini: {'Mevcut' if self.log_dir.exists() else 'Eksik'} 
- ⚠️ Yanlış yerdeki dosyalar: {result['misplaced_files']}

## 🚨 Tespit Edilen Sorunlar

"""
        
        if result["issues"]:
            for i, issue in enumerate(result["issues"], 1):
                report += f"{i}. **{issue['type']}:** {issue['file']}\n"
                report += f"   └─ {issue['message']}\n\n"
        else:
            report += "✅ Sorun bulunamadı! Proje organizasyonu temiz.\n\n"
            
        if self.fixes_applied:
            report += "## ✅ Uygulanan Düzeltmeler\n\n"
            for fix in self.fixes_applied:
                report += f"- {fix}\n"
            report += "\n"
            
        report += """
## 🛡️ Önleyici Önlemler

1. **Git Hook Kurulumu:**
   ```bash
   # Pre-commit hook olarak kur
   cp system_improvement_meta_project/meta_project_guard.py .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. **Manuel Kontrol:**
   ```bash
   python system_improvement_meta_project/meta_project_guard.py --check
   ```

3. **Otomatik Düzeltme:**
   ```bash
   python system_improvement_meta_project/meta_project_guard.py --fix
   ```

---
**Oluşturan:** Meta-Proje Koruma Sistemi v1.0
"""
        
        return report
        
    def save_report(self, report: str):
        """Raporu dosyaya kaydet"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.log_dir / f"meta_project_guard_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📝 Rapor kaydedildi: {report_path}")
        return report_path

def main():
    parser = argparse.ArgumentParser(description="Meta-Proje Koruma Sistemi")
    parser.add_argument("--check", action="store_true", help="Sadece kontrol et")
    parser.add_argument("--fix", action="store_true", help="Sorunları düzelt")
    parser.add_argument("--git-hook", action="store_true", help="Git hook modu")
    parser.add_argument("--report", action="store_true", help="Detaylı rapor oluştur")
    
    args = parser.parse_args()
    
    guard = MetaProjectGuard()
    
    if args.git_hook:
        # Git hook modu - commit'i engelle veya geçir
        if not guard.git_hook_check():
            exit(1)  # Commit'i engelle
        exit(0)
        
    elif args.fix:
        print("🔧 Meta-proje sorunları düzeltiliyor...")
        result = guard.fix_issues()
        print(f"✅ Durum: {result['status']}")
        
        if result.get('fixes_applied'):
            print("\n📝 Uygulanan düzeltmeler:")
            for fix in result['fixes_applied']:
                print(f"  - {fix}")
                
    elif args.report:
        print("📊 Detaylı rapor oluşturuluyor...")
        report = guard.generate_report()
        guard.save_report(report)
        print(report)
        
    else:  # Default: check
        print("🔍 Meta-proje organizasyonu kontrol ediliyor...")
        result = guard.check_project_isolation()
        print(f"📊 Durum: {result['status']}")
        print(f"🚨 Toplam sorun: {result['total_issues']}")
        
        if result['issues']:
            print("\n⚠️ Tespit edilen sorunlar:")
            for issue in result['issues']:
                print(f"  - {issue['file']}: {issue['message']}")
        else:
            print("✅ Proje organizasyonu temiz!")

if __name__ == "__main__":
    main() 