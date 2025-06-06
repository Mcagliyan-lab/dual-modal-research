# Dual-Modal Neural Network Neuroimaging Framework

Bu proje, yapay sinir ağlarının iç işleyişini, hem zamansal (NN-EEG) hem de uzamsal (NN-fMRI) boyutlarda analiz eden yenilikçi bir çerçeve sunar. Amacımız, derin öğrenme modellerinin karar verme süreçlerini ve dahili temsillerini, insan beynindeki aktivite desenlerini anlamaya benzer şekilde yorumlayabilmek ve görselleştirebilmektir.

---

## 🎯 **Proje Durumu: Academic Publication Preparation Phase**

**📊 Ana Başarı:** 91.66% ±0.05% cross-modal consistency (CIFAR-10 dataset)  
**🚀 Mevcut Faz:** Academic publication preparation + Hybrid system planning  
**⏰ Son Güncelleme:** 2025-06-06  

### **Core Implementation Tamamlandı ✅**
- ✅ **NN-EEG Temporal Analysis:** FFT-based frequency domain processing
- ✅ **NN-fMRI Spatial Analysis:** Grid-based activation density calculation  
- ✅ **Dual-Modal Integration:** 91.66% cross-modal consistency achieved
- ✅ **CIFAR-10 Validation:** Statistical significance proven, reproducible results
- ✅ **Production Framework:** Well-documented Python implementation

---

## Temel Özellikler

- **NN-fMRI (Uzamsal Analiz):** Sinir ağlarının aktivasyonlarını 3D uzamsal ızgaralara eşleyerek kritik bölgeleri ve bilgi akış yollarını belirler.
- **NN-EEG (Zamansal Analiz):** Sinir ağlarının dinamik zaman serisi davranışlarını analiz ederek, karar alma süreçlerindeki zamansal desenleri ve anormallikleri ortaya çıkarır.
- **Çift Modlu Entegrasyon:** Hem uzamsal hem de zamansal analizlerden elde edilen bilgileri birleştirerek, ağın işleyişine dair kapsamlı bir yorum sunar.
- **Görselleştirme Araçları:** Analiz sonuçlarını kolayca yorumlamak için zengin görselleştirmeler sağlar (örn. aktivasyon haritaları, bağlantı traktografları).
- **Esneklik ve Genişletilebilirlik:** Çeşitli ağ mimarileri ve görevler için uyarlanabilir, yeni analiz tekniklerinin entegrasyonuna açıktır.

---

## 📈 **Performans Metrikleri**

### **Mevcut Python Implementation:**
- **Cross-Modal Consistency:** 91.66% ± 0.05% (CIFAR-10)
- **Processing Time:** 58.96 seconds per analysis
- **Memory Usage:** ~25 MB peak usage
- **Code Quality:** Production-ready, 95%+ documentation coverage

### **Planned Hybrid C++/Python Optimization:**
- **Target Performance:** 16-18 seconds (3.3-3.7x improvement)
- **Memory Efficiency:** 20-30% reduction expected
- **Real-time Goal:** <1s per analysis capability
- **Large Model Support:** ResNet-50+, Vision Transformers

---

## Mimariye Genel Bakış

Çerçeve, sinir ağı aktivasyonlarını işleyen, analiz eden ve görselleştiren modüler bileşenlerden oluşur. Veri akışı genellikle şöyledir:

1.  **Veri Girişi:** Eğitilmiş bir sinir ağı modeli ve girdi verileri sisteme sağlanır.
2.  **Aktivasyon Çıkarımı:** Modelin farklı katmanlarından ve nöronlarından ara aktivasyonlar çıkarılır.
3.  **NN-fMRI İşleme:** Çıkarılan aktivasyonlar uzamsal ızgaralara dönüştürülür ve kritik bölgelerin ζ-skorları hesaplanır.
4.  **NN-EEG İşleme:** Aktivasyonların zamansal dinamikleri analiz edilir ve zaman serisi desenleri belirlenir.
5.  **Çift Modlu Birleştirme:** Uzamsal ve zamansal analiz sonuçları entegre edilir.
6.  **Görselleştirme ve Raporlama:** Birleştirilmiş sonuçlar, görselleştirmeler ve detaylı raporlar halinde sunulur.

---

## 🚀 **Gelecek Roadmap**

### **Immediate (Next 2-4 Weeks): Academic Publication**
- Complete paper draft (discussion, conclusion, references)
- MNIST and Fashion-MNIST validation experiments  
- Submit to IEEE/ACM tier-1 venue

### **Short-term (Next 2-3 Months): Performance Optimization**
- Hybrid C++/Python implementation
- FFTW-based FFT optimization + Eigen/BLAS integration
- Large model support (ResNet-50+, Transformers)

### **Long-term (Next 6+ Months): Applications**
- Medical AI applications (HAM10000 skin lesion analysis)
- NLP model adaptation (BERT/RoBERTa)
- Real-time deployment capabilities
- Open source community development

---

## Hızlı Başlangıç
Projeyi kurmak ve çalıştırmak için lütfen kapsamlı [Başlangıç Kılavuzu](docs/getting-started.md) bölümümüze göz atın. Bu kılavuz, kurulum adımlarından temel kullanım senaryolarına kadar projenizi ayağa kaldırmak için ihtiyacınız olan her şeyi detaylandırır.

## Dokümantasyon
Projenin tüm detaylı dokümantasyonuna erişmek için:
- [Proje Analiz Raporu](project_docs/proje_analiz_raporu.md)
- [AI Session Notes](project_docs/ai_session_notes.md)
- [Task Progress Tracking](project_docs/task_progress.md)
- [Problem/Solution Log](project_docs/problem_solution_log.md)
- [Teorik Temeller](theory/framework-overview.md)
- [Kullanım Örnekleri](examples/ADVANCED_USAGE.md)
- [Terimler Sözlüğü](theory/GLOSSARY.md)

---

## 🛡️ **YAPYÖS v2.0 Meta-Project Integration**

Bu ana proje, **YAPYÖS v2.0 (Yapay Zeka Proje Yönetim Sistemi)** meta-project framework'ü ile geliştirilmiştir:

### **Meta-Project Benefits:**
- **%100 Autonomous Operation:** AI script execution with intelligent risk management
- **Session Continuity:** Persistent memory across conversation interruptions
- **Context Management:** Zero knowledge loss with SQLite-based persistence
- **Quality Assurance:** Automated linting, validation, documentation
- **Problem Tracking:** Systematic problem-solution documentation

### **Session Continuity Usage:**
```bash
# New conversation'da proje durumunu restore etmek için:
python system_improvement_meta_project/context_demo.py

# Manual restore:
from system_improvement_meta_project.context_manager import ContextManager
manager = ContextManager("YAPYOS_v2")
session = manager.resume_session()
summary = manager.generate_context_summary()
print(summary)
```

### **Meta-Project Documentation:**
- [YAPYÖS Complete Story (TR)](system_improvement_meta_project/YAPYOS_META_PROJECT_COMPLETE_STORY.md)
- [YAPYÖS Complete Story (EN)](system_improvement_meta_project/YAPYOS_META_PROJECT_COMPLETE_STORY_EN.md)
- [Final Usage Guide](system_improvement_meta_project/README_FINAL_GUIDE.md)

---

## Katkıda Bulunma
Projeye nasıl katkıda bulunabileceğinizi öğrenmek için [Katkıda Bulunma Kılavuzu](project_docs/CONTRIBUTING.md) dosyasını inceleyin.

---

**🎯 Current Focus:** Academic publication preparation with 91.66% cross-modal consistency results  
**🚀 Next Milestone:** Paper submission to tier-1 venue + C++/Python hybrid system development  
**🛡️ Project Management:** Enhanced with YAPYÖS v2.0 autonomous AI project management infrastructure 