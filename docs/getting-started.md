# 🚀 Getting Started with Dual-Modal Neuroimaging

## Quick Start Guide

### Installation

Bu projeyi yerel makinenizde kurmak ve çalıştırmak için aşağıdaki adımları izleyin.

**1. Depoyu Klonlayın:**

```bash
git clone https://github.com/Mcagliyan-lab/dual-modal-research
cd dual-modal-research
```

**2. Sanal Ortam Oluşturun ve Etkinleştirin (Önerilen):

**A. Conda ile:**

Eğer [Conda](https://docs.conda.io/en/latest/miniconda.html) kullanıyorsanız, `environment.yml` dosyasını kullanarak bir ortam oluşturabilirsiniz:

```bash
conda env create -f environment.yml
conda activate dual-modal-neuroimaging
```

**B. Python venv ile:**

Alternatif olarak, Python'ın yerleşik `venv` modülünü kullanabilirsiniz:

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

**3. Bağımlılıkları Yükleyin:**

Sanal ortamınızı etkinleştirdikten sonra gerekli Python bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
```

### Basic Usage

Bu bölümde, temel NN-EEG, NN-fMRI ve çift modlu entegrasyon analizlerini nasıl çalıştırabileceğinizi bulacaksınız.

```python
import torch
from torch.utils.data import DataLoader, TensorDataset

# Basit bir örnek model oluşturun
class SimpleNN(torch.nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.linear1 = torch.nn.Linear(10, 20)
        self.relu = torch.nn.ReLU()
        self.linear2 = torch.nn.Linear(20, 1)

    def forward(self, x):
        return self.linear2(self.relu(self.linear1(x)))

model = SimpleNN()

# Örnek veri oluşturun (Gerçek kullanımda kendi verilerinizi yükleyeceksiniz)
n_samples = 100
n_features = 10
dummy_data = torch.randn(n_samples, n_features)
dummy_labels = torch.randn(n_samples, 1)
dummy_dataset = TensorDataset(dummy_data, dummy_labels)
dataloader = DataLoader(dummy_dataset, batch_size=10)
```

#### NN-EEG Temporal Analysis
```python
from src.nn_neuroimaging.nn_eeg.implementation import NeuralEEG

# Analizciyi oluşturun
analyzer = NeuralEEG(model)

# Zamansal dinamikleri analiz edin
temporal_signals = analyzer.extract_temporal_signals(dataloader)
print(f"Çıkarılan zamansal sinyal şekli: {temporal_signals.shape}")
# Beklenen Çıktı: Katmanlardan çıkarılan zamansal aktivasyon verilerini içeren bir tensör.

frequency_results = analyzer.analyze_frequency_domain()
print(f"Frekans alanı sonuçları: {frequency_results.keys()}")
# Beklenen Çıktı: Farklı frekans bantları ve ilgili güç spektrumları gibi frekans analiz sonuçlarını içeren bir sözlük.

state = analyzer.classify_operational_states()
print(f"Operasyonel durum sınıflandırması: {state}")
# Beklenen Çıktı: Modelin operasyonel durumunun bir sınıflandırması (örn. 'stabil', 'dalgalı').
```

#### NN-fMRI Spatial Analysis
```python
from src.nn_neuroimaging.nn_fmri.implementation import NeuralFMRI

# Uzamsal analizciyi oluşturun
spatial_analyzer = NeuralFMRI(model)

# Uzamsal desenleri analiz edin
spatial_results = spatial_analyzer.analyze_spatial_patterns(dummy_data)
print(f"Uzamsal analiz sonuçlarının anahtarları: {spatial_results.keys()}")
# Beklenen Çıktı: Uzamsal aktivasyon haritaları ve yoğunlukları gibi uzamsal analiz sonuçlarını içeren bir sözlük.

zeta_scores = spatial_analyzer.compute_zeta_scores(dummy_data)
print(f"Zeta skorları şekli: {zeta_scores.shape}")
# Beklenen Çıktı: Her bir uzamsal bölge için hesaplanan zeta skorlarını içeren bir tensör.
```

#### Dual-Modal Integration
```python
from src.nn_neuroimaging.integration.framework import DualModalIntegrator

# Tam analizi gerçekleştirin
integrator = DualModalIntegrator(model)
results = integrator.analyze(dummy_data)
print(f"Entegre analiz sonuçlarının anahtarları: {results.keys()}")
# Beklenen Çıktı: Hem zamansal hem de uzamsal analizlerden entegre edilmiş sonuçları içeren bir sözlük.
```

## Examples

See `examples/` directory for complete working examples:
- `examples/quick_start.py` - Basic dual-modal demonstration

## Status

- ✅ NN-EEG: Working and tested
- ✅ NN-fMRI: Working and tested  
- ✅ Integration: Complete and validated

## Support

Check `docs/troubleshooting.md` for common issues.
