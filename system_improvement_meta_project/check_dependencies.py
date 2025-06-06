#!/usr/bin/env python3
"""
Bağımlılık Kontrol ve Kurulum Scripti
====================================

Bu script, YAPYÖS için gerekli bağımlılıkları kontrol eder ve eksik olanları yükler.

Kullanım:
    python check_dependencies.py [--install] [--check-only] [--verbose]
"""

import sys
import subprocess
import importlib
import json
import os
import platform
from typing import List, Dict, Tuple, Optional

class DependencyChecker:
    def __init__(self, verbose: bool = False):
        """Bağımlılık kontrol sınıfını başlatır."""
        self.verbose = verbose
        self.missing_packages = []
        self.outdated_packages = []
        self.system_info = self.get_system_info()
        
        # Gerekli Python paketleri
        self.required_packages = {
            'json': 'Built-in',
            'os': 'Built-in', 
            'sys': 'Built-in',
            'datetime': 'Built-in',
            'pathlib': 'Built-in',
            're': 'Built-in',
            'argparse': 'Built-in',
            'typing': 'Built-in'
        }
        
        # Opsiyonel paketler (eğer requirements.txt varsa)
        self.optional_packages = [
            'pytest',
            'black',
            'flake8',
            'mypy',
            'mkdocs',
            'mkdocs-material'
        ]

    def get_system_info(self) -> Dict[str, str]:
        """Sistem bilgilerini toplar."""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation()
        }

    def log(self, message: str, level: str = "INFO") -> None:
        """Verbose mod aktifse mesaj yazdırır."""
        if self.verbose or level == "ERROR":
            print(f"[{level}] {message}")

    def check_python_version(self) -> bool:
        """Python sürümünü kontrol eder."""
        min_version = (3, 8)
        current_version = sys.version_info[:2]
        
        if current_version < min_version:
            self.log(f"Python {min_version[0]}.{min_version[1]}+ gerekli. Mevcut: {current_version[0]}.{current_version[1]}", "ERROR")
            return False
        
        self.log(f"Python sürümü OK: {current_version[0]}.{current_version[1]}")
        return True

    def check_package(self, package_name: str) -> bool:
        """Belirli bir paketin yüklenip yüklenmediğini kontrol eder."""
        try:
            importlib.import_module(package_name)
            self.log(f"Package '{package_name}' bulundu")
            return True
        except ImportError:
            self.log(f"Package '{package_name}' bulunamadı", "ERROR")
            self.missing_packages.append(package_name)
            return False

    def check_requirements_file(self, requirements_file: str = "requirements.txt") -> List[str]:
        """requirements.txt dosyasından paketleri okur."""
        packages = []
        if os.path.exists(requirements_file):
            with open(requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Versiyonları çıkar (>=, ==, etc.)
                        package = line.split('>=')[0].split('==')[0].split('<')[0].split('>')[0]
                        packages.append(package.strip())
            self.log(f"'{requirements_file}' dosyasından {len(packages)} paket bulundu")
        else:
            self.log(f"'{requirements_file}' dosyası bulunamadı")
        return packages

    def install_package(self, package_name: str) -> bool:
        """Eksik paketi pip ile yükler."""
        try:
            self.log(f"Package '{package_name}' yükleniyor...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package_name
            ], capture_output=True, text=True, check=True)
            self.log(f"Package '{package_name}' başarıyla yüklendi")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Package '{package_name}' yüklenirken hata: {e.stderr}", "ERROR")
            return False

    def check_docker_availability(self) -> bool:
        """Docker'ın kullanılabilir olup olmadığını kontrol eder."""
        try:
            result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"Docker bulundu: {result.stdout.strip()}")
                return True
            else:
                self.log("Docker bulunamadı")
                return False
        except FileNotFoundError:
            self.log("Docker kurulu değil")
            return False

    def check_git_availability(self) -> bool:
        """Git'in kullanılabilir olup olmadığını kontrol eder."""
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"Git bulundu: {result.stdout.strip()}")
                return True
            else:
                self.log("Git bulunamadı")
                return False
        except FileNotFoundError:
            self.log("Git kurulu değil")
            return False

    def generate_report(self) -> Dict[str, any]:
        """Durum raporu oluşturur."""
        return {
            'system_info': self.system_info,
            'python_version_ok': self.check_python_version(),
            'docker_available': self.check_docker_availability(),
            'git_available': self.check_git_availability(),
            'missing_packages': self.missing_packages,
            'outdated_packages': self.outdated_packages,
            'total_issues': len(self.missing_packages) + len(self.outdated_packages)
        }

    def run_full_check(self, auto_install: bool = False) -> bool:
        """Tam bağımlılık kontrolü yapar."""
        self.log("=== YAPYÖS Bağımlılık Kontrolü Başlatılıyor ===")
        
        # Python sürümü kontrolü
        if not self.check_python_version():
            return False

        # Built-in paketleri kontrol et
        self.log("Built-in Python paketleri kontrol ediliyor...")
        for package in self.required_packages:
            self.check_package(package)

        # requirements.txt'den paketleri kontrol et
        req_packages = self.check_requirements_file()
        for package in req_packages:
            self.check_package(package)

        # Opsiyonel paketleri kontrol et
        self.log("Opsiyonel paketler kontrol ediliyor...")
        for package in self.optional_packages:
            if not self.check_package(package):
                # Opsiyonel paketler için missing_packages'dan çıkar
                if package in self.missing_packages:
                    self.missing_packages.remove(package)

        # Eksik paketleri yükle
        if auto_install and self.missing_packages:
            self.log(f"{len(self.missing_packages)} eksik paket yükleniyor...")
            for package in self.missing_packages[:]:  # Copy to avoid modification during iteration
                if self.install_package(package):
                    self.missing_packages.remove(package)

        # Diğer araçları kontrol et
        self.check_docker_availability()
        self.check_git_availability()

        # Sonuç
        if self.missing_packages:
            self.log(f"Eksik paketler: {', '.join(self.missing_packages)}", "ERROR")
            return False
        else:
            self.log("Tüm gerekli bağımlılıklar mevcut ✅")
            return True

def main():
    """Ana fonksiyon."""
    import argparse
    
    parser = argparse.ArgumentParser(description="YAPYÖS bağımlılık kontrolü")
    parser.add_argument("--install", action="store_true", 
                        help="Eksik paketleri otomatik yükle")
    parser.add_argument("--check-only", action="store_true",
                        help="Sadece kontrol et, yükleme yapma")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Detaylı çıktı")
    parser.add_argument("--report", type=str,
                        help="JSON raporu kaydetmek için dosya yolu")
    
    args = parser.parse_args()
    
    checker = DependencyChecker(verbose=args.verbose)
    
    # Ana kontrolü çalıştır
    auto_install = args.install and not args.check_only
    success = checker.run_full_check(auto_install=auto_install)
    
    # Rapor oluştur
    report = checker.generate_report()
    
    if args.report:
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Rapor kaydedildi: {args.report}")
    
    # Özet yazdır
    print("\n=== ÖZET ===")
    print(f"Python: {report['python_version_ok']} ✅" if report['python_version_ok'] else "Python: ❌")
    print(f"Docker: {report['docker_available']} ✅" if report['docker_available'] else "Docker: ❌")  
    print(f"Git: {report['git_available']} ✅" if report['git_available'] else "Git: ❌")
    print(f"Eksik paketler: {len(report['missing_packages'])}")
    print(f"Toplam sorun: {report['total_issues']}")
    
    if success:
        print("🎉 Tüm bağımlılıklar hazır!")
        sys.exit(0)
    else:
        print("⚠️  Bazı bağımlılıklar eksik!")
        sys.exit(1)

if __name__ == "__main__":
    main() 