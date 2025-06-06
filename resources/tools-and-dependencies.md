# 🛠️ Araçlar ve Bağımlılıklar

Dual-Modal Neural Network Neuroimaging Framework projesi, geliştirilmesi ve çalışması için çeşitli yazılım araçlarına ve kütüphanelerine bağımlıdır. Bu bölüm, projenin temel bağımlılıklarını ve kullanılan yardımcı araçları listelemektedir.

## 1. Temel Yazılım Bağımlılıkları (Python Kütüphaneleri)

Projenin çalışması için gerekli olan Python kütüphaneleri `requirements.txt` dosyasında listelenmiştir. İşte başlıca olanlar:

*   **PyTorch:** Derin öğrenme modellerini oluşturmak ve çalıştırmak için ana framework. Nöral ağ aktivasyonlarını yakalamak ve işlemek için kullanılır.
*   **NumPy:** Sayısal hesaplamalar için temel kütüphane. Özellikle sinyal işleme ve veri manipülasyonunda yaygın olarak kullanılır.
*   **SciPy:** Bilimsel ve teknik hesaplamalar için Python kütüphanesi. Sinyal işleme (özellikle Welch yöntemi için), istatistik ve diğer bilimsel fonksiyonlar için kullanılır.
*   **Matplotlib:** Veri görselleştirmesi için Python kütüphanesi. Analiz sonuçlarını (frekans spektrumları, uzamsal desenler) grafiksel olarak sunmak için kullanılır.
*   **Torchvision:** Bilgisayar görüşü alanındaki veri setleri (CIFAR-10, MNIST) ve model mimarileri için yardımcı kütüphane.
*   **PyYAML:** Yapılandırma dosyalarını (`config.yaml`) okumak ve yazmak için kullanılır.
*   **Pandas:** Veri manipülasyonu ve analizi için (raporlama ve sonuçların işlenmesinde potansiyel kullanım).

## 2. Geliştirme ve Dokümantasyon Araçları

Projenin geliştirme süreci ve dokümantasyonu için kullanılan araçlar:

*   **Git:** Sürüm kontrol sistemi.
*   **GitHub/GitLab:** Kod deposu yönetimi ve işbirliği platformu.
*   **pytest:** Projedeki birim ve entegrasyon testlerini çalıştırmak için kullanılan Python test framework'ü.
*   **flake8 / Black:** Kod stili ve linting için Python araçları. Kodun okunabilirliğini ve tutarlılığını sağlamak için kullanılır.
*   **MkDocs:** Statik site oluşturucu. Tüm `.md` dokümantasyon dosyalarını bir web sitesi olarak yayınlamak için kullanılır.
*   **MkDocs Material:** MkDocs için modern ve duyarlı bir tema.
*   **mkdocstrings:** Python kodundaki docstringlerden otomatik olarak API dokümantasyonu oluşturmak için MkDocs eklentisi.
*   **Jupyter / JupyterLab:** Etkileşimli kod geliştirme, deneyler ve eğitim not defterleri oluşturmak için (özellikle `examples/notebooks/` bölümünde potansiyel kullanım).

## 3. Ortam Yönetimi

Projenin bağımlılıklarının izole ve yönetilebilir bir ortamda kurulması için aşağıdaki araçlar önerilir:

*   **conda / Miniconda / Anaconda:** Sanal ortam oluşturma ve paket yönetimi için.
*   **pip:** Python paketlerini yüklemek için standart araç.

## Kurulum Talimatları

Bu bağımlılıkların nasıl kurulacağına dair detaylı talimatlar için lütfen [Başlangıç Kılavuzu](docs/getting-started.md) belgesine bakın.

Bu liste, projenin bağımlılıkları ve kullanılan araçlar hakkında genel bir bakış sunmaktadır ve projenin gelişimiyle birlikte güncellenebilir.
