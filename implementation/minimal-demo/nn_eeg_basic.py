"""
Neural Network Electroencephalography (NN-EEG) Implementation
=============================================================

Core implementation of temporal dynamics analysis for neural networks.
This is a working proof-of-concept that demonstrates the theoretical framework.

Author: Independent Research
Date: December 22, 2024
Version: 0.1.0 (Minimal Viable Implementation)

IMPORTANT: This implements the theoretical framework described in our paper.
           Results are preliminary but reproducible.
"""

import torch
import torch.nn as nn
import numpy as np
from scipy import signal
from scipy.stats import pearsonr
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class ActivationCapture:
    """
    Captures layer activations during forward pass for temporal analysis.
    This is the foundation of our NN-EEG approach.
    """

    def __init__(self, model: nn.Module, layer_types: tuple = (nn.Conv2d, nn.Linear)):
        self.model = model
        self.layer_types = layer_types
        self.activations = {}
        self.hooks = []
        self.temporal_buffer = []
        self._register_hooks()

    def _register_hooks(self):
        """Register forward hooks on specified layer types"""
        def create_hook(name):
            def hook_fn(module, input, output):
                # Convert to numpy and aggregate spatial dimensions
                activation = output.detach().cpu().numpy()

                # Aggregate based on tensor dimensions
                if len(activation.shape) == 4:  # Conv layers (B, C, H, W)
                    aggregated = np.mean(activation, axis=(0, 2, 3))  # Keep channels
                elif len(activation.shape) == 2:  # Linear layers (B, F)
                    aggregated = np.mean(activation, axis=0)  # Keep features
                else:
                    aggregated = np.mean(activation)  # Fallback to scalar

                self.activations[name] = aggregated
            return hook_fn

        # Register hooks on target layers
        layer_count = 0
        for name, module in self.model.named_modules():
            if isinstance(module, self.layer_types):
                hook = module.register_forward_hook(create_hook(f"layer_{layer_count}_{name}"))
                self.hooks.append(hook)
                layer_count += 1

        print(f"Registered hooks on {layer_count} layers")

    def capture_batch_activations(self, data_batch: torch.Tensor) -> Dict[str, np.ndarray]:
        """Capture activations for a single batch"""
        self.activations.clear()

        with torch.no_grad():
            _ = self.model(data_batch)

        return dict(self.activations)

    def cleanup(self):
        """Remove all hooks"""
        for hook in self.hooks:
            hook.remove()
        self.hooks.clear()

class NeuralEEG:
    """
    Main NN-EEG analyzer implementing temporal dynamics analysis.

    This class implements the core concepts from our theoretical framework:
    - Temporal signal extraction from layer activations
    - Frequency domain analysis using Welch's method
    - Operational state classification based on spectral patterns
    """

    def __init__(self, model: nn.Module, sample_rate: float = 1.0):
        self.model = model
        self.sample_rate = sample_rate
        self.activation_capture = ActivationCapture(model)

        # Frequency bands (adapted from EEG neuroscience)
        self.frequency_bands = {
            'delta': (0.5, 4),     # Deep processing
            'theta': (4, 8),       # Memory/learning
            'alpha': (8, 13),      # Idle states
            'beta': (13, 30),      # Active processing
            'gamma': (30, 100)     # High-level cognition
        }

        # Analysis parameters
        self.window_size = 50      # Number of samples for analysis
        self.overlap_ratio = 0.5   # Window overlap for Welch's method

        # Results storage
        self.temporal_signals = {}
        self.frequency_analysis = {}
        self.state_classifications = []

    def extract_temporal_signals(self, dataloader, max_batches: int = 50) -> Dict[str, np.ndarray]:
        """
        Extract temporal signals from neural network activations.

        This is the core NN-EEG process: treating layer activations as
        time series data for frequency analysis.
        """
        print(f"Extracting temporal signals from {max_batches} batches...")

        temporal_data = {}
        batch_count = 0

        #start_time = time.time() # time import needed for this line

        for batch_idx, (data, targets) in enumerate(dataloader):
            if batch_count >= max_batches:
                break

            # Capture activations for this batch
            activations = self.activation_capture.capture_batch_activations(data)

            # Store temporal progression
            for layer_name, activation in activations.items():
                if layer_name not in temporal_data:
                    temporal_data[layer_name] = []

                # Convert to scalar signal (mean of all neurons/channels)
                if isinstance(activation, np.ndarray):
                    signal_value = np.mean(activation)
                else:
                    signal_value = float(activation)

                temporal_data[layer_name].append(signal_value)

            batch_count += 1

            # Progress indicator
            if batch_count % 10 == 0:
                print(f"  Processed {batch_count} batches...")

        # Convert lists to numpy arrays
        for layer_name in temporal_data:
            temporal_data[layer_name] = np.array(temporal_data[layer_name])

        #processing_time = time.time() - start_time # time import needed for this line
        #print(f"Temporal signal extraction completed in {processing_time:.2f}s") # time import needed for this line

        self.temporal_signals = temporal_data
        return temporal_data

    def analyze_frequency_domain(self, temporal_signals: Optional[Dict[str, np.ndarray]] = None) -> Dict[str, Dict]:
        """
        Perform frequency domain analysis using Welch's method.

        This implements the spectral analysis core of NN-EEG methodology.
        """
        if temporal_signals is None:
            temporal_signals = self.temporal_signals

        if not temporal_signals:
            raise ValueError("No temporal signals available. Run extract_temporal_signals first.")

        print("Performing frequency domain analysis...")

        frequency_results = {}

        for layer_name, temporal_signal in temporal_signals.items():
            if len(temporal_signal) < 10:  # Skip layers with insufficient data
                continue

            try:
                # Apply Welch's method for power spectral density
                nperseg = min(len(temporal_signal) // 4, 16)  # Adaptive window size
                if nperseg < 4:
                    nperseg = len(temporal_signal)

                frequencies, psd = signal.welch(
                    temporal_signal,
                    fs=self.sample_rate,
                    nperseg=nperseg,
                    noverlap=None if nperseg == len(temporal_signal) else nperseg//2
                )

                # Extract frequency band powers
                band_powers = self._extract_band_powers(frequencies, psd)

                # Compute spectral features
                spectral_features = self._compute_spectral_features(frequencies, psd)

                frequency_results[layer_name] = {
                    'frequencies': frequencies,
                    'power_spectral_density': psd,
                    'band_powers': band_powers,
                    'spectral_features': spectral_features,
                    'dominant_frequency': frequencies[np.argmax(psd)],
                    'total_power': np.sum(psd)
                }

            except Exception as e:
                print(f"Warning: Could not analyze {layer_name}: {e}")
                raise e

        self.frequency_analysis = frequency_results
        return frequency_results

    def _extract_band_powers(self, frequencies: np.ndarray, psd: np.ndarray) -> Dict[str, float]:
        """Extract power in each frequency band"""
        band_powers = {}

        for band_name, (low_freq, high_freq) in self.frequency_bands.items():
            # Find frequency indices in this band
            band_mask = (frequencies >= low_freq) & (frequencies <= high_freq)

            if np.any(band_mask):
                band_power = np.sum(psd[band_mask])
            else:
                band_power = 0.0

            band_powers[band_name] = band_power

        return band_powers

    def _compute_spectral_features(self, frequencies: np.ndarray, psd: np.ndarray) -> Dict[str, float]:
        """Compute additional spectral features"""
        return {
            'spectral_centroid': np.sum(frequencies * psd) / np.sum(psd) if np.sum(psd) > 0 else 0,
            'spectral_entropy': self._spectral_entropy(psd),
            'peak_frequency': frequencies[np.argmax(psd)],
            'bandwidth': self._spectral_bandwidth(frequencies, psd)
        }

    def _spectral_entropy(self, psd: np.ndarray) -> float:
        """Compute spectral entropy"""
        # Normalize PSD to create probability distribution
        psd_norm = psd / (np.sum(psd) + 1e-12)
        psd_norm = psd_norm[psd_norm > 0]  # Remove zeros

        if len(psd_norm) <= 1:
            return 0.0

        return -np.sum(psd_norm * np.log2(psd_norm))

    def _spectral_bandwidth(self, frequencies: np.ndarray, psd: np.ndarray) -> float:
        """Compute spectral bandwidth"""
        if np.sum(psd) == 0:
            return 0.0

        centroid = np.sum(frequencies * psd) / np.sum(psd)
        bandwidth = np.sqrt(np.sum(((frequencies - centroid) ** 2) * psd) / np.sum(psd))
        return bandwidth

    def classify_operational_states(self, frequency_analysis: Optional[Dict] = None) -> str: # Changed return type to str based on usage
        """
        Classify operational states based on frequency patterns.

        This implements our state classification methodology using spectral signatures.
        """
        if frequency_analysis is None:
            frequency_analysis = self.frequency_analysis

        if not frequency_analysis:
            raise ValueError("No frequency analysis available. Run analyze_frequency_domain first.")

        print("Classifying operational states...")

        # Aggregate across all layers for global state assessment
        global_band_powers = {band: 0.0 for band in self.frequency_bands.keys()}
        layer_count = 0

        for layer_name, analysis in frequency_analysis.items():
            if 'band_powers' in analysis:
                for band, power in analysis['band_powers'].items():
                    global_band_powers[band] += power
                layer_count += 1

        # Normalize by number of layers
        if layer_count > 0:
            for band in global_band_powers:
                global_band_powers[band] /= layer_count

        # State classification logic based on spectral patterns
        state = self._determine_state_from_spectrum(global_band_powers)

        # Note: The original code appended to self.state_classifications here,
        # but that seems more appropriate for the experiment/demonstration script.
        # Returning the state string directly for use in the experiment script.

        return state # Return state string

    def _determine_state_from_spectrum(self, band_powers: Dict[str, float]) -> str:
        """Determine operational state from frequency band powers"""

        # Normalize band powers
        total_power = sum(band_powers.values())
        if total_power == 0:
            return 'idle'

        normalized_powers = {band: power/total_power for band, power in band_powers.items()}

        # State classification rules (based on our theoretical framework)
        gamma_ratio = normalized_powers['gamma']
        beta_ratio = normalized_powers['beta']
        alpha_ratio = normalized_powers['alpha']
        theta_ratio = normalized_powers['theta']

        # High gamma indicates intensive processing (training-like)
        if gamma_ratio > 0.4:
            return 'training'

        # High beta indicates active inference
        elif beta_ratio > 0.3:
            return 'inference'

        # High alpha indicates idle state
        elif alpha_ratio > 0.5:
            return 'idle'

        # Irregular patterns suggest error state
        elif max(normalized_powers.values()) < 0.3:  # No dominant frequency
            return 'error'

        else:
            return 'inference'  # Default to inference state

    def _compute_state_confidence(self, band_powers: Dict[str, float]) -> float:
        """Compute confidence in state classification"""
        total_power = sum(band_powers.values())
        if total_power == 0:
            return 0.0

        normalized_powers = list(band_powers.values())
        normalized_powers = [p/total_power for p in normalized_powers]

        # Confidence based on how dominant the strongest frequency band is
        max_power = max(normalized_powers)
        return min(max_power * 2, 1.0)  # Scale to [0, 1]

    def generate_report(self) -> Dict:
        """Generate comprehensive analysis report"""

        report = {
            #'analysis_timestamp': datetime.now().isoformat(), # datetime import needed
            'model_info': {
                'type': type(self.model).__name__,
                'total_parameters': sum(p.numel() for p in self.model.parameters()),
                'layers_analyzed': len(self.temporal_signals)
            },
            'temporal_analysis': {
                'signal_length': len(list(self.temporal_signals.values())[0]) if self.temporal_signals else 0,
                'sampling_rate': self.sample_rate,
                'window_size': self.window_size
            },
            'frequency_analysis_summary': {},
            #'state_classifications': self.state_classifications, # Moved to experiment script
            'layer_statistics': {}
        }

        # Summarize frequency analysis
        if self.frequency_analysis:
            all_dominant_freqs = []
            all_total_powers = []

            for layer_name, analysis in self.frequency_analysis.items():
                all_dominant_freqs.append(analysis['dominant_frequency'])
                all_total_powers.append(analysis['total_power'])

                # Per-layer statistics
                report['layer_statistics'][layer_name] = {
                    'dominant_frequency': analysis['dominant_frequency'],
                    'total_power': analysis['total_power'],
                    'spectral_entropy': analysis['spectral_features']['spectral_entropy']
                }

            report['frequency_analysis_summary'] = {
                'mean_dominant_frequency': np.mean(all_dominant_freqs),
                'std_dominant_frequency': np.std(all_dominant_freqs),
                'mean_total_power': np.mean(all_total_powers),
                'layers_analyzed': len(all_dominant_freqs)
            }

        return report

    def visualize_results(self): # Removed save_path parameter, visualization handled in experiment script
        """Prepare visualization data for NN-EEG analysis results"""

        if not self.frequency_analysis:
            print("No frequency analysis results to visualize.")
            return None # Return None if no data

        # Prepare data for visualization (e.g., returning frequency and PSD data)
        # The actual plotting will be done in the experiment script
        visualization_data = {}
        for layer_name, analysis in self.frequency_analysis.items():
             visualization_data[layer_name] = {
                 'frequencies': analysis['frequencies'].tolist(), # Convert to list for easier handling
                 'power_spectral_density': analysis['power_spectral_density'].tolist(),
                 'dominant_frequency': float(analysis['dominant_frequency']), # Ensure serializable
                 'frequency_bands': self.frequency_bands # Include bands for plotting
             }

        return visualization_data # Return data for plotting

    def cleanup(self):
        """Clean up resources"""
        self.activation_capture.cleanup()

# Removed demonstration/testing functions and __main__ block
