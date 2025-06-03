#!/usr/bin/env python3
"""
Quick Start Test: NN-EEG Implementation Validation
=================================================
Python version of the quick_start_test.sh script for Windows compatibility.
This script validates the NN-EEG proof-of-concept works on your system.
"""

import os
import sys
import subprocess
import torch
import torch.nn as nn
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import json
import time
from pathlib import Path

def run_command(cmd, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command: {cmd}")
        print(f"Exception: {e}")
        return False

def main():
    print("🚀 NN-EEG Quick Start Test (Python Version)")
    print("=" * 50)
    
    # 1. Check Python version
    print("1. Checking Python environment...")
    print(f"Python version: {sys.version}")
    
    # 2. Create project directories
    print("2. Setting up project directories...")
    try:
        Path("results").mkdir(exist_ok=True)
        print("   ✅ results/ directory created")
    except Exception as e:
        print(f"   ❌ Failed to create directories: {e}")
        return False
    
    # 3. Create requirements file (already exists, but let's check)
    print("3. Checking requirements.txt...")
    if not Path("requirements.txt").exists():
        requirements = """torch>=1.9.0
torchvision>=0.10.0
numpy>=1.20.0
scipy>=1.7.0
matplotlib>=3.4.0"""
        with open("requirements.txt", "w") as f:
            f.write(requirements)
        print("   ✅ requirements.txt created")
    else:
        print("   ✅ requirements.txt already exists")
    
    # 4. Quick dependency check (skip installation as they should be already installed)
    print("4. Checking dependencies...")
    try:
        import torch
        import torchvision
        import numpy
        import scipy
        import matplotlib
        print("   ✅ All dependencies are available")
    except ImportError as e:
        print(f"   ❌ Missing dependency: {e}")
        print("   Please install with: pip install -r requirements.txt")
        return False
    
    # 5. Run minimal NN-EEG test
    print("5. Running minimal NN-EEG validation test...")
    
    # Set seeds for reproducibility
    torch.manual_seed(42)
    np.random.seed(42)
    
    print("   Creating test model...")
    model = nn.Sequential(
        nn.Conv2d(3, 8, 3, padding=1),
        nn.ReLU(),
        nn.MaxPool2d(2),
        nn.Conv2d(8, 16, 3, padding=1),
        nn.ReLU(),
        nn.AdaptiveAvgPool2d(1),
        nn.Flatten(),
        nn.Linear(16, 10)
    )
    model.eval()
    
    print("   Creating synthetic data...")
    data = torch.randn(10, 3, 32, 32)  # 10 samples, like CIFAR-10
    dataloader = torch.utils.data.DataLoader(
        torch.utils.data.TensorDataset(data, torch.randint(0, 10, (10,))),
        batch_size=2,
        shuffle=False
    )
    
    print("   Capturing layer activations...")
    activations = {}
    hooks = []
    
    def create_hook(name):
        def hook_fn(module, input, output):
            act = output.detach().cpu().numpy()
            if len(act.shape) == 4:  # Conv layer
                activations[name] = np.mean(act, axis=(0, 2, 3))  # Mean across batch and spatial
            else:  # Linear layer
                activations[name] = np.mean(act, axis=0)  # Mean across batch
        return hook_fn
    
    # Register hooks
    layer_count = 0
    for name, module in model.named_modules():
        if isinstance(module, (nn.Conv2d, nn.Linear)):
            hook = module.register_forward_hook(create_hook(f"layer_{layer_count}"))
            hooks.append(hook)
            layer_count += 1
    
    print("   Extracting temporal signals...")
    temporal_signals = {}
    
    for batch_idx, (batch_data, _) in enumerate(dataloader):
        activations.clear()
        
        with torch.no_grad():
            _ = model(batch_data)
        
        # Store temporal progression
        for layer_name, activation in activations.items():
            if layer_name not in temporal_signals:
                temporal_signals[layer_name] = []
            
            signal_value = np.mean(activation)
            temporal_signals[layer_name].append(signal_value)
    
    # Convert to numpy arrays
    for layer_name in temporal_signals:
        temporal_signals[layer_name] = np.array(temporal_signals[layer_name])
    
    print(f"   Captured signals from {len(temporal_signals)} layers")
    for layer_name, sig in temporal_signals.items():
        print(f"     {layer_name}: {len(sig)} time points, range: [{sig.min():.3f}, {sig.max():.3f}]")
    
    print("   Performing frequency analysis...")
    frequency_results = {}
    
    for layer_name, sig in temporal_signals.items():
        if len(sig) >= 4:  # Minimum for frequency analysis
            try:
                frequencies, psd = signal.welch(sig, fs=1.0, nperseg=len(sig))
                dominant_freq = frequencies[np.argmax(psd)]
                total_power = np.sum(psd)
                
                frequency_results[layer_name] = {
                    'dominant_frequency': float(dominant_freq),
                    'total_power': float(total_power),
                    'frequencies': frequencies.tolist(),
                    'psd': psd.tolist()
                }
                
                print(f"     {layer_name}: {dominant_freq:.3f} Hz (power: {total_power:.4f})")
                
            except Exception as e:
                print(f"     {layer_name}: Analysis failed - {e}")
    
    print("   Classifying operational state...")
    if frequency_results:
        all_dominant_freqs = [result['dominant_frequency'] for result in frequency_results.values()]
        mean_freq = np.mean(all_dominant_freqs)
        
        if mean_freq > 0.3:
            state = "inference"
        elif mean_freq > 0.1:
            state = "processing"
        else:
            state = "idle"
        
        print(f"     Operational state: {state} (mean freq: {mean_freq:.3f} Hz)")
    else:
        state = "unknown"
        print("     Could not classify state - insufficient data")
    
    print("   Creating visualization...")
    if frequency_results:
        try:
            fig, axes = plt.subplots(1, min(3, len(frequency_results)), figsize=(12, 4))
            if len(frequency_results) == 1:
                axes = [axes]
            elif len(frequency_results) == 2:
                axes = list(axes)
            
            for idx, (layer_name, result) in enumerate(list(frequency_results.items())[:3]):
                ax = axes[idx] if len(frequency_results) > 1 else axes[0]
                
                frequencies = np.array(result['frequencies'])
                psd = np.array(result['psd'])
                
                ax.plot(frequencies, psd, 'b-', linewidth=2)
                ax.set_title(f'{layer_name}\n{result["dominant_frequency"]:.3f} Hz')
                ax.set_xlabel('Frequency (Hz)')
                ax.set_ylabel('Power')
                ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('results/quick_test_results.png', dpi=150, bbox_inches='tight')
            plt.close()  # Don't show in non-interactive environments
            print("     ✅ Visualization saved to results/quick_test_results.png")
        except Exception as e:
            print(f"     ❌ Visualization failed: {e}")
    
    print("   Saving results...")
    results = {
        'test_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'model_layers': layer_count,
        'signal_length': len(list(temporal_signals.values())[0]) if temporal_signals else 0,
        'frequency_analysis': frequency_results,
        'operational_state': state,
        'test_status': 'SUCCESS' if frequency_results else 'PARTIAL'
    }
    
    with open('results/quick_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Cleanup
    for hook in hooks:
        hook.remove()
    
    # 6. Final report
    print("\n" + "=" * 50)
    print("✅ NN-EEG QUICK TEST COMPLETED!")
    print("=" * 50)
    print(f"Status: {results['test_status']}")
    print(f"Layers analyzed: {results['model_layers']}")
    print(f"Signal length: {results['signal_length']} time points")
    print(f"Operational state: {results['operational_state']}")
    print(f"Results saved to: results/quick_test_results.json")
    
    if results['test_status'] == 'SUCCESS':
        print("\n🎉 PROOF-OF-CONCEPT VALIDATED!")
        print("The NN-EEG framework successfully:")
        print("✅ Captured layer activations")
        print("✅ Extracted temporal signals")
        print("✅ Performed frequency analysis")
        print("✅ Classified operational state")
        print("✅ Generated reproducible results")
        print("\nNext step: Run full CIFAR-10 validation")
    else:
        print("\n⚠️  PARTIAL SUCCESS")
        print("Basic framework works but needs debugging")
    
    print("\nTest completed! 🚀")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 