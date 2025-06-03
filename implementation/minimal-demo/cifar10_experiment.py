import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Import the core NN-EEG analysis class
from .nn_eeg_basic import NeuralEEG

def create_test_model() -> nn.Module:
    """Create a simple CNN for testing NN-EEG"""
    model = nn.Sequential(
        nn.Conv2d(3, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(16, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(32, 64, kernel_size=3, padding=1), 
        nn.ReLU(),
        nn.AdaptiveAvgPool2d((1, 1)),
        nn.Flatten(),
        nn.Linear(64, 128),
        nn.ReLU(),
        nn.Linear(128, 10)
    )
    return model

def run_cifar10_demonstration():
    """
    Complete demonstration of NN-EEG on CIFAR-10 dataset.
    This provides reproducible proof-of-concept results.
    """
    print("=" * 60)
    print("NN-EEG CIFAR-10 DEMONSTRATION")
    print("=" * 60)
    
    # Set random seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    # Create model
    print("1. Creating test model...")
    model = create_test_model()
    model.eval()  # Set to evaluation mode
    
    # Load CIFAR-10 dataset
    print("2. Loading CIFAR-10 dataset...")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    
    dataset = torchvision.datasets.CIFAR10(
        root='./data', 
        train=False, 
        download=True, 
        transform=transform
    )
    
    dataloader = torch.utils.data.DataLoader(
        dataset, 
        batch_size=32, 
        shuffle=False  # Deterministic for reproducibility
    )
    
    # Initialize NN-EEG analyzer
    print("3. Initializing NN-EEG analyzer...")
    analyzer = NeuralEEG(model, sample_rate=1.0)
    
    # Extract temporal signals
    print("4. Extracting temporal signals...")
    temporal_signals = analyzer.extract_temporal_signals(dataloader, max_batches=30)
    
    print(f"   Captured signals from {len(temporal_signals)} layers")
    for layer_name, signal in temporal_signals.items():
        print(f"   {layer_name}: {len(signal)} time points")
    
    # Perform frequency analysis
    print("5. Performing frequency domain analysis...")
    frequency_results = analyzer.analyze_frequency_domain()
    
    print(f"   Analyzed {len(frequency_results)} layers")
    
    # Classify operational state
    print("6. Classifying operational state...")
    current_state = analyzer.classify_operational_states()
    print(f"   Current operational state: {current_state}")
    
    # Generate comprehensive report
    print("7. Generating analysis report...")
    report = analyzer.generate_report()
    
    # Display key results
    print("\n" + "=" * 60)
    print("KEY RESULTS")
    print("=" * 60)
    
    print(f"Model: {report['model_info']['type']}")
    print(f"Parameters: {report['model_info']['total_parameters']:,}")
    print(f"Layers analyzed: {report['model_info']['layers_analyzed']}")
    print(f"Signal length: {report['temporal_analysis']['signal_length']} time points")
    
    if report['frequency_analysis_summary']:
        freq_summary = report['frequency_analysis_summary']
        print(f"Mean dominant frequency: {freq_summary['mean_dominant_frequency']:.2f} ± {freq_summary['std_dominant_frequency']:.2f} Hz")
        print(f"Mean total power: {freq_summary['mean_total_power']:.4f}")
    
    print(f"Current operational state: {current_state}")
    
    # Show layer-wise results
    print("\nLayer-wise Analysis:")
    for layer_name, stats in report['layer_statistics'].items():
        print(f"  {layer_name}: {stats['dominant_frequency']:.2f} Hz, Power: {stats['total_power']:.4f}")
    
    # Visualize results
    print("\n8. Creating visualizations...")
    analyzer.visualize_results()
    
    # Save results
    print("9. Saving results...")
    with open('nn_eeg_cifar10_results.json', 'w') as f:
        # Convert numpy arrays to lists for JSON serialization
        json_report = report.copy()
        for layer_name, stats in json_report['layer_statistics'].items():
            for key, value in stats.items():
                if isinstance(value, np.ndarray):
                    stats[key] = value.tolist()
                elif isinstance(value, (np.float32, np.float64)):
                    stats[key] = float(value)
        
        json.dump(json_report, f, indent=2, default=str)
    
    print("   Results saved to 'nn_eeg_cifar10_results.json'")
    
    # Cleanup
    analyzer.cleanup()
    
    print("\n" + "=" * 60)
    print("NN-EEG DEMONSTRATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    return report

if __name__ == "__main__":
    # Run the complete demonstration
    results = run_cifar10_demonstration()
    
    print("\nDemonstration completed. Results available in 'nn_eeg_cifar10_results.json'")
    print("This provides reproducible proof-of-concept validation of NN-EEG methodology.")
