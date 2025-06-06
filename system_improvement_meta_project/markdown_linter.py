#!/usr/bin/env python3
"""
YAPYÖS Markdown Linting Sistemi
===============================

Bu script, proje belgelerindeki Markdown formatı, yer tutucular ve tutarlılığı kontrol eder.

Kullanım:
    python markdown_linter.py [--fix] [--config config.json] [--output report.md]
"""

import os
import re
import json
import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Any

class MarkdownLinter:
    def __init__(self, config_path: str = "project_config.json"):
        """Markdown linter sınıfını başlatır."""
        self.config_path = config_path
        self.config = self.load_config()
        self.issues = []
        self.placeholders_found = set()
        self.expected_placeholders = self.get_expected_placeholders()
        
        # Linting kuralları
        self.rules = {
            'heading_consistency': True,
            'placeholder_validation': True,
            'line_length': 120,
            'trailing_whitespace': True,
            'empty_lines': True,
            'link_validation': True,
            'markdown_syntax': True
        }

    def load_config(self) -> Dict[str, Any]:
        """Proje yapılandırmasını yükler."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Uyarı: {self.config_path} bulunamadı. Varsayılan değerler kullanılıyor.")
            return {}

    def get_expected_placeholders(self) -> set:
        """Beklenen yer tutucuları döndürür."""
        return {
            '[PROJE_ADI]',
            '[KRITIK_ODAK_ALANI]', 
            '[PROJE_ANALIZ_RAPORU_DOSYASI]',
            '[PROJE_CALISMA_PLANI_DOSYASI]',
            '[AI_OTURUM_NOTLARI_DOSYASI]',
            '[PROBLEM_COZUM_LOG_DOSYASI]',
            '[AI_TODO_LIST_DOSYASI]',
            '[TASK_PROGRESS_DOSYASI]',
            '[UYARI_RAPORU_DOSYASI]',
            '[ILK_CALISMA_PLANI_FAZI_BASLIGI]',
            '[GUNCEL_PROJE_DURUMU]',
            '[OTURUM_TARIHI]'
        }

    def add_issue(self, file_path: str, line_num: int, rule: str, message: str, severity: str = "WARNING") -> None:
        """Sorun ekler."""
        self.issues.append({
            'file': file_path,
            'line': line_num,
            'rule': rule,
            'message': message,
            'severity': severity
        })

    def check_heading_consistency(self, content: str, file_path: str) -> None:
        """Başlık tutarlılığını kontrol eder."""
        lines = content.split('\n')
        heading_levels = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                heading_levels.append((i, level, line.strip()))
                
                # Başlık formatı kontrolü
                if not re.match(r'^#+\s+\S', line.strip()):
                    self.add_issue(file_path, i, 'heading_format', 
                                 f"Başlık formatı hatalı: '{line.strip()}' (# sonrasında boşluk olmalı)")

        # Başlık seviye atlama kontrolü
        for i in range(1, len(heading_levels)):
            prev_level = heading_levels[i-1][1]
            curr_level = heading_levels[i][1]
            
            if curr_level - prev_level > 1:
                line_num = heading_levels[i][0]
                self.add_issue(file_path, line_num, 'heading_sequence',
                             f"Başlık seviyesi atlanmış: H{prev_level}'den H{curr_level}'e geçiş")

    def check_placeholder_validation(self, content: str, file_path: str) -> None:
        """Yer tutucu doğrulaması yapar."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Yer tutucuları bul
            placeholders = re.findall(r'\[([A-Z_]+)\]', line)
            for placeholder in placeholders:
                full_placeholder = f'[{placeholder}]'
                self.placeholders_found.add(full_placeholder)
                
                # Beklenmeyen yer tutucu kontrolü
                if full_placeholder not in self.expected_placeholders:
                    self.add_issue(file_path, i, 'unknown_placeholder',
                                 f"Bilinmeyen yer tutucu: {full_placeholder}")

    def check_line_length(self, content: str, file_path: str) -> None:
        """Satır uzunluğunu kontrol eder."""
        lines = content.split('\n')
        max_length = self.rules['line_length']
        
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                self.add_issue(file_path, i, 'line_length',
                             f"Satır çok uzun: {len(line)} karakter (maksimum: {max_length})")

    def check_trailing_whitespace(self, content: str, file_path: str) -> None:
        """Satır sonlarındaki boşlukları kontrol eder."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            if line.rstrip() != line:
                self.add_issue(file_path, i, 'trailing_whitespace',
                             "Satır sonunda gereksiz boşluk")

    def check_empty_lines(self, content: str, file_path: str) -> None:
        """Boş satır kurallarını kontrol eder."""
        lines = content.split('\n')
        consecutive_empty = 0
        
        for i, line in enumerate(lines, 1):
            if line.strip() == '':
                consecutive_empty += 1
                if consecutive_empty > 2:
                    self.add_issue(file_path, i, 'excessive_empty_lines',
                                 f"Çok fazla ardışık boş satır: {consecutive_empty}")
            else:
                consecutive_empty = 0

    def check_link_validation(self, content: str, file_path: str) -> None:
        """Link formatını kontrol eder."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Markdown link formatı
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)
            for link_text, link_url in links:
                if not link_text.strip():
                    self.add_issue(file_path, i, 'empty_link_text',
                                 "Link metni boş")
                
                # Yerel dosya linklerini kontrol et
                if not link_url.startswith(('http://', 'https://', 'mailto:', '#')):
                    if not os.path.exists(link_url):
                        self.add_issue(file_path, i, 'broken_link',
                                     f"Kırık link: {link_url}")

    def check_markdown_syntax(self, content: str, file_path: str) -> None:
        """Temel Markdown sözdizimini kontrol eder."""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Kalın yazı formatı kontrolü
            if '**' in line:
                bold_count = line.count('**')
                if bold_count % 2 != 0:
                    self.add_issue(file_path, i, 'unclosed_bold',
                                 "Kapatılmamış kalın yazı formatı (**)")
            
            # İtalik yazı formatı kontrolü
            single_asterisk = re.findall(r'(?<!\*)\*(?!\*)', line)
            if len(single_asterisk) % 2 != 0:
                self.add_issue(file_path, i, 'unclosed_italic',
                             "Kapatılmamış italik yazı formatı (*)")
            
            # Liste formatı kontrolü
            if re.match(r'^\s*[-*+]\s*$', line):
                self.add_issue(file_path, i, 'empty_list_item',
                             "Boş liste öğesi")

    def lint_file(self, file_path: str) -> None:
        """Tek bir dosyayı lint'ler."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            self.add_issue(file_path, 1, 'encoding_error',
                         "UTF-8 encoding hatası", "ERROR")
            return

        if self.rules['heading_consistency']:
            self.check_heading_consistency(content, file_path)
        
        if self.rules['placeholder_validation']:
            self.check_placeholder_validation(content, file_path)
        
        if self.rules['line_length']:
            self.check_line_length(content, file_path)
        
        if self.rules['trailing_whitespace']:
            self.check_trailing_whitespace(content, file_path)
        
        if self.rules['empty_lines']:
            self.check_empty_lines(content, file_path)
        
        if self.rules['link_validation']:
            self.check_link_validation(content, file_path)
        
        if self.rules['markdown_syntax']:
            self.check_markdown_syntax(content, file_path)

    def find_markdown_files(self, directory: str = ".") -> List[str]:
        """Dizindeki Markdown dosyalarını bulur."""
        markdown_files = []
        
        for root, dirs, files in os.walk(directory):
            # .git ve node_modules klasörlerini atla
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith(('.md', '.markdown')):
                    markdown_files.append(os.path.join(root, file))
        
        return markdown_files

    def generate_report(self, output_path: str = "lint_report.md") -> None:
        """Lint raporu oluşturur."""
        # İstatistikler
        error_count = len([i for i in self.issues if i['severity'] == 'ERROR'])
        warning_count = len([i for i in self.issues if i['severity'] == 'WARNING'])
        
        # Dosya bazında grupla
        files_with_issues = {}
        for issue in self.issues:
            file_path = issue['file']
            if file_path not in files_with_issues:
                files_with_issues[file_path] = []
            files_with_issues[file_path].append(issue)

        report_content = f"""# YAPYÖS Markdown Linting Raporu

**Rapor Tarihi:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Tarama Dizini:** {os.getcwd()}

---

## 📊 Özet

| Metrik | Değer |
|--------|-------|
| Toplam Dosya | {len(files_with_issues)} |
| Toplam Sorun | {len(self.issues)} |
| Hata | {error_count} |
| Uyarı | {warning_count} |

---

## 🔍 Bulunan Yer Tutucular

"""
        
        if self.placeholders_found:
            for placeholder in sorted(self.placeholders_found):
                status = "✅" if placeholder in self.expected_placeholders else "❌"
                report_content += f"- {status} {placeholder}\n"
        else:
            report_content += "Hiç yer tutucu bulunamadı.\n"

        report_content += "\n---\n\n## 📋 Dosya Bazında Sorunlar\n\n"

        if files_with_issues:
            for file_path, file_issues in files_with_issues.items():
                report_content += f"### {file_path}\n\n"
                
                for issue in file_issues:
                    severity_icon = "🚨" if issue['severity'] == 'ERROR' else "⚠️"
                    report_content += f"- **Satır {issue['line']}:** {severity_icon} [{issue['rule']}] {issue['message']}\n"
                
                report_content += "\n"
        else:
            report_content += "✅ Hiç sorun bulunamadı!\n"

        report_content += """
---

## 📋 Öneriler

### Yüksek Öncelikli
- Hata seviyesindeki sorunları derhal giderin
- Kırık linkleri düzeltin
- Encoding sorunlarını çözün

### Orta Öncelikli
- Başlık seviye tutarlılığını sağlayın
- Uzun satırları bölün
- Satır sonlarındaki boşlukları temizleyin

### Düşük Öncelikli
- Çok fazla boş satırları azaltın
- Liste formatlarını düzeltin

---

**Bu rapor `markdown_linter.py` scripti tarafından otomatik olarak oluşturulmuştur.**
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"Lint raporu oluşturuldu: {output_path}")

    def run_linting(self, directory: str = ".", output_file: str = "lint_report.md") -> bool:
        """Ana linting işlemini çalıştırır."""
        print("🔍 YAPYÖS Markdown Linting başlatılıyor...")
        
        markdown_files = self.find_markdown_files(directory)
        print(f"  ✓ {len(markdown_files)} Markdown dosyası bulundu")
        
        for file_path in markdown_files:
            print(f"  🔍 Kontrol ediliyor: {file_path}")
            self.lint_file(file_path)
        
        self.generate_report(output_file)
        
        error_count = len([i for i in self.issues if i['severity'] == 'ERROR'])
        warning_count = len([i for i in self.issues if i['severity'] == 'WARNING'])
        
        print(f"✅ Linting tamamlandı:")
        print(f"   📁 {len(markdown_files)} dosya tarandı")
        print(f"   🚨 {error_count} hata")
        print(f"   ⚠️  {warning_count} uyarı")
        
        return error_count == 0

def main():
    """Ana fonksiyon."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YAPYÖS Markdown linting")
    parser.add_argument("--directory", "-d", default=".", 
                        help="Taranacak dizin")
    parser.add_argument("--config", default="project_config.json",
                        help="Yapılandırma dosyası")
    parser.add_argument("--output", "-o", default="lint_report.md",
                        help="Çıktı raporu dosyası")
    parser.add_argument("--fix", action="store_true",
                        help="Otomatik düzeltme (gelecek versiyon)")
    
    args = parser.parse_args()
    
    linter = MarkdownLinter(args.config)
    success = linter.run_linting(args.directory, args.output)
    
    exit_code = 0 if success else 1
    exit(exit_code)

if __name__ == "__main__":
    main() 