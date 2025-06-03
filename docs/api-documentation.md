# 📖 API Documentation

## NN-EEG Module

### NeuralEEG Class

**Main temporal analysis class**

#### `__init__(model, sample_rate=1.0)`
Initialize NN-EEG analyzer
- `model`: PyTorch neural network
- `sample_rate`: Sampling rate for frequency analysis

#### `extract_temporal_signals(dataloader, max_batches=50)`
Extract temporal signals from layer activations
- Returns: Dictionary of layer-wise temporal signals

#### `analyze_frequency_domain(temporal_signals=None)`
Perform frequency domain analysis
- Returns: Frequency analysis results with PSD and band powers

#### `classify_operational_states(frequency_analysis=None)`
Classify network operational state
- Returns: State classification ('training', 'inference', 'idle', 'error')

## NN-fMRI Module (Coming Soon)

### NeuralFMRI Class

**Main spatial analysis class**

#### `__init__(model, grid_size=(8,8,4))`
Initialize NN-fMRI analyzer
- `model`: PyTorch neural network  
- `grid_size`: 3D grid dimensions for spatial partitioning

#### `analyze_spatial_patterns(data)`
Analyze spatial activation patterns
- Returns: Spatial analysis results

#### `compute_zeta_scores(validation_data)`
Compute impact scores for spatial regions
- Returns: ζ-scores for each grid region

## Integration Module (Coming Soon)

### DualModalIntegrator Class

**Combined temporal + spatial analysis**

#### `__init__(model)`
Initialize dual-modal analyzer

#### `analyze(data, report_type='technical')`
Complete dual-modal analysis
- Returns: Comprehensive analysis results

## Utility Modules

### Data Loaders
- `cifar10_loader()`: CIFAR-10 dataset
- `mnist_loader()`: MNIST dataset  
- `synthetic_loader()`: Synthetic test data

### Visualization
- `plot_frequency_analysis()`: NN-EEG results
- `plot_spatial_grids()`: NN-fMRI results
- `create_dual_modal_dashboard()`: Combined visualization

### Metrics
- `DualModalMetrics`: Evaluation metrics
- `statistical_significance_test()`: Statistical testing
