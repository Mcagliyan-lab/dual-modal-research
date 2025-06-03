# 🚀 Getting Started with Dual-Modal Neuroimaging

## Quick Start Guide

### Installation
```bash
git clone https://github.com/Mcagliyan-lab/dual-modal-research
cd dual-modal-research
pip install -r requirements.txt
```

### Basic Usage

#### NN-EEG Temporal Analysis
```python
from implementation.minimal_demo.nn_eeg_basic import NeuralEEG
import torch

# Create model and analyzer
model = torch.nn.Sequential(...)
analyzer = NeuralEEG(model)

# Analyze temporal dynamics
temporal_signals = analyzer.extract_temporal_signals(dataloader)
frequency_results = analyzer.analyze_frequency_domain()
state = analyzer.classify_operational_states()
```

#### NN-fMRI Spatial Analysis (Coming Soon)
```python
from implementation.minimal_demo.nn_fmri_basic import NeuralFMRI

# Create spatial analyzer
spatial_analyzer = NeuralFMRI(model)

# Analyze spatial patterns
spatial_results = spatial_analyzer.analyze_spatial_patterns(data)
zeta_scores = spatial_analyzer.compute_zeta_scores(validation_data)
```

#### Dual-Modal Integration (Coming Soon)
```python
from implementation.minimal_demo.integration import DualModalIntegrator

# Complete analysis
integrator = DualModalIntegrator(model)
results = integrator.analyze(data)
```

## Examples

See `examples/` directory for complete working examples.

## Status

- ✅ NN-EEG: Working and tested
- 🟡 NN-fMRI: Implementation in progress
- ⏳ Integration: Planned after NN-fMRI complete

## Support

Check `docs/troubleshooting.md` for common issues.
