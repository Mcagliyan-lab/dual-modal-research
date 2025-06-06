#!/usr/bin/env python3
"""
YAPYÖS Ortam Kurulum Scripti
===========================

Bu script, YAPYÖS (Yapay Zeka Proje Yönetim Sistemi) için tam ortam kurulumu yapar.

Kullanım:
    python setup_environment.py [--docker] [--full] [--meta-project]
"""

import sys
import os
import subprocess
import json
import datetime
from pathlib import Path

class EnvironmentSetup:
    def __init__(self, verbose: bool = True):
        """Ortam kurulum sınıfını başlatır."""
        self.verbose = verbose
        self.project_root = Path.cwd()
        self.logs = []

    def log(self, message: str, level: str = "INFO") -> None:
        """Log mesajı ekler ve yazdırır."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        
        if self.verbose:
            print(log_entry)

    def run_command(self, command: list, description: str) -> bool:
        """Komut çalıştırır ve sonucu döndürür."""
        try:
            self.log(f"Çalıştırılıyor: {description}")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            if result.stdout:
                self.log(f"Çıktı: {result.stdout.strip()}")
            
            self.log(f"✅ Başarılı: {description}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Hata: {description} - {e.stderr}", "ERROR")
            return False

    def check_prerequisites(self) -> bool:
        """Ön koşulları kontrol eder."""
        self.log("=== ÖN KOŞUL KONTROLLERI ===")
        
        # Python sürümü
        python_version = sys.version_info
        if python_version >= (3, 8):
            self.log(f"✅ Python {python_version.major}.{python_version.minor} uygun")
        else:
            self.log(f"❌ Python 3.8+ gerekli, mevcut: {python_version.major}.{python_version.minor}", "ERROR")
            return False

        # Pip kontrolü
        if self.run_command([sys.executable, "-m", "pip", "--version"], "Pip kontrolü"):
            pass
        else:
            return False

        return True

    def install_dependencies(self) -> bool:
        """Bağımlılıkları yükler."""
        self.log("=== BAĞIMLILIK KURULUMU ===")
        
        # requirements.txt varsa yükle
        if Path("requirements.txt").exists():
            if not self.run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                   "requirements.txt bağımlılıkları"):
                return False

        # requirements-dev.txt varsa yükle
        if Path("requirements-dev.txt").exists():
            if not self.run_command([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], 
                                   "Development bağımlılıkları"):
                return False

        return True

    def setup_directories(self) -> bool:
        """Gerekli dizinleri oluşturur."""
        self.log("=== DİZİN KURULUMU ===")
        
        directories = [
            "logs",
            "output", 
            "data",
            "project_docs",
            "system_improvement_meta_project"
        ]
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                self.log(f"✅ Dizin oluşturuldu: {directory}")
            else:
                self.log(f"ℹ️  Dizin mevcut: {directory}")

        return True

    def setup_docker(self) -> bool:
        """Docker ortamını hazırlar."""
        self.log("=== DOCKER KURULUMU ===")
        
        # Docker kontrolü
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                self.log("❌ Docker bulunamadı", "ERROR") 
                return False
            self.log(f"✅ Docker bulundu: {result.stdout.strip()}")
        except FileNotFoundError:
            self.log("❌ Docker kurulu değil", "ERROR")
            return False

        # Docker build
        if not self.run_command(["docker", "build", "-t", "yapyos:latest", "."], "Docker image build"):
            return False

        # Docker test
        if not self.run_command(["docker", "run", "--rm", "yapyos:latest", "python", "-c", "print('Docker test OK')"], 
                               "Docker container test"):
            return False

        return True

    def setup_meta_project(self) -> bool:
        """Meta-proje kurulumunu yapar."""
        self.log("=== META-PROJE KURULUMU ===")
        
        # Meta-proje dizini
        meta_dir = Path("system_improvement_meta_project")
        meta_dir.mkdir(exist_ok=True)
        
        # auto_setup_script.py çalıştır
        setup_script = meta_dir / "auto_setup_script.py"
        if setup_script.exists():
            if not self.run_command([sys.executable, str(setup_script)], "Meta-proje auto setup"):
                return False
        else:
            self.log("⚠️  auto_setup_script.py bulunamadı", "WARNING")

        return True

    def run_tests(self) -> bool:
        """Test suite çalıştırır."""
        self.log("=== TEST ÇALIŞTIRMA ===")
        
        # otomatik_gorev_kontrolu.py testi
        if Path("otomatik_gorev_kontrolu.py").exists():
            if not self.run_command([sys.executable, "otomatik_gorev_kontrolu.py", "--help"], 
                                   "Görev kontrol scripti testi"):
                return False

        # Bağımlılık kontrol testi
        if Path("check_dependencies.py").exists():
            if not self.run_command([sys.executable, "check_dependencies.py", "--check-only"], 
                                   "Bağımlılık kontrol testi"):
                self.log("⚠️  Bazı bağımlılıklar eksik olabilir", "WARNING")

        return True

    def generate_setup_report(self) -> None:
        """Kurulum raporu oluşturur."""
        self.log("=== KURULUM RAPORU ===")
        
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "setup_logs": self.logs,
            "files_created": [],
            "directories_created": [],
            "status": "completed"
        }
        
        # Oluşturulan dosyaları tespit et
        important_files = [
            "otomatik_gorev_kontrolu.py",
            "check_dependencies.py", 
            "setup_environment.py",
            "Dockerfile",
            "docker-compose.yml"
        ]
        
        for file_path in important_files:
            if Path(file_path).exists():
                report["files_created"].append(file_path)

        # Raporu kaydet
        report_path = Path("logs") / "setup_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Kurulum raporu kaydedildi: {report_path}")

    def run_full_setup(self, include_docker: bool = False, include_meta: bool = True) -> bool:
        """Tam kurulum işlemini çalıştırır."""
        self.log("🚀 YAPYÖS ORTAM KURULUMU BAŞLATILIYOR")
        
        success = True
        
        # Ön koşullar
        if not self.check_prerequisites():
            success = False

        # Dizin kurulumu
        if success and not self.setup_directories():
            success = False

        # Bağımlılık kurulumu
        if success and not self.install_dependencies():
            success = False

        # Docker kurulumu (isteğe bağlı)
        if success and include_docker:
            if not self.setup_docker():
                self.log("⚠️  Docker kurulumu başarısız, devam ediliyor", "WARNING")

        # Meta-proje kurulumu
        if success and include_meta:
            if not self.setup_meta_project():
                success = False

        # Testler
        if success:
            if not self.run_tests():
                self.log("⚠️  Bazı testler başarısız, ama kurulum tamamlandı", "WARNING")

        # Rapor oluştur
        self.generate_setup_report()

        if success:
            self.log("🎉 KURULUM BAŞARIYLA TAMAMLANDI!")
            self.log("📋 Sonraki adımlar:")
            self.log("   1. python otomatik_gorev_kontrolu.py --help")
            self.log("   2. python check_dependencies.py --verbose")
            if include_docker:
                self.log("   3. docker-compose up yapyos-main")
        else:
            self.log("❌ KURULUM BAŞARISIZ", "ERROR")

        return success

def main():
    """Ana fonksiyon."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YAPYÖS ortam kurulumu")
    parser.add_argument("--docker", action="store_true", 
                        help="Docker kurulumu da yap")
    parser.add_argument("--full", action="store_true",
                        help="Tam kurulum (Docker dahil)")
    parser.add_argument("--meta-project", action="store_true", default=True,
                        help="Meta-proje kurulumunu yap")
    parser.add_argument("--quiet", action="store_true",
                        help="Sessiz mod")
    
    args = parser.parse_args()
    
    verbose = not args.quiet
    setup = EnvironmentSetup(verbose=verbose)
    
    include_docker = args.docker or args.full
    include_meta = args.meta_project
    
    success = setup.run_full_setup(
        include_docker=include_docker,
        include_meta=include_meta
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 