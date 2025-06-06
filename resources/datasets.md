# 🗄️ Veri Setleri

Dual-Modal Neural Network Neuroimaging Framework projesi, farklı model mimarileri ve kullanım senaryoları üzerinde doğrulanmak üzere çeşitli veri setlerini kullanmaktadır. İşte projenin odaklandığı ve potansiyel olarak kullanılabilecek veri setleri:

## 1. Birincil Doğrulama Veri Setleri

### 1.1 CIFAR-10
*   **Açıklama:** 10 farklı sınıfa ait (uçak, otomobil, kuş, kedi, geyik, köpek, kurbağa, at, gemi, kamyon) 60.000 adet 32x32 renkli görüntüden oluşan yaygın bir bilgisayar görüşü veri setidir. Eğitim için 50.000, test için 10.000 görüntü içerir.
*   **Kullanım Amacı:** Çift modlu çerçevenin temel doğrulaması, çapraz modal tutarlılık testleri ve gerçek zamanlı performans değerlendirmeleri için kullanılmıştır.
*   **Proje Bağlantısı:** Projenin `results/` dizinindeki doğrulamalarda ve makale sonuçlarında kullanılmıştır.

### 1.2 MNIST
*   **Açıklama:** El yazısı rakamlardan (0-9) oluşan 70.000 gri tonlamalı görüntüden oluşan popüler bir veri setidir. Eğitim için 60.000, test için 10.000 görüntü içerir.
*   **Kullanım Amacı:** Temel model doğrulaması ve performans kıyaslaması için bir başlangıç veri seti olarak kullanılmıştır.
*   **Proje Bağlantısı:** Projenin `data/MNIST/` dizininde bulunmaktadır.

### 1.3 Sentetik Veri Setleri
*   **Açıklama:** Özel test senaryoları ve çerçevenin belirli özelliklerini izole etmek için programlı olarak oluşturulan yapay veri setleri.
*   **Kullanım Amacı:** Çerçevenin belirli bileşenlerinin (örneğin, frekans analizi, uzamsal bölümleme) kontrollü koşullar altında doğrulanması.
*   **Proje Bağlantısı:** Özellikle geliştirme ve birim test aşamalarında kullanılmıştır.

## 2. Potansiyel Gelecek Veri Setleri

### 2.1 HAM10000 (Human Against Machine with 10000 training images)
*   **Açıklama:** Dermatolojik görüntülerden (deri lezyonları) oluşan büyük bir veri setidir. Yedi farklı deri kanseri kategorisini içerir.
*   **Kullanım Amacı:** Çerçevenin tıbbi görüntüleme ve sağlık uygulamalarındaki potansiyelini keşfetmek ve klinik veri setleri üzerinde doğrulamak.
*   **Önemi:** Projenin klinik uygulamalara genişlemesi için kritik bir adımdır.

### 2.2 Diğer Nörogörüntüleme Veri Setleri (EEG/fMRI)
*   **Açıklama:** Gerçek EEG (Elektroensefalografi) ve fMRI (Fonksiyonel Manyetik Rezonans Görüntüleme) verileri.
*   **Kullanım Amacı:** Sinir ağı davranışlarını gerçek biyolojik nöral aktivite ile karşılaştırmak ve çerçevenin nörobilimdeki yorumlanabilirliğini artırmak.
*   **Önemi:** Nörobilim ve yapay zeka arasındaki köprüyü güçlendirmek için temel.

## Veri Seti Kullanım Notları

*   Tüm veri setleri, ilgili lisans koşullarına uygun olarak kullanılmalıdır.
*   Büyük veri setleri için, proje klasörüne indirme betikleri veya talimatları sağlanacaktır.
*   Veri seti işleme ve yükleme adımları, `src/nn_neuroimaging/utils/data_loaders.py` modülünde detaylandırılmıştır.

Projenin kapsamı genişledikçe bu liste güncellenecektir.
