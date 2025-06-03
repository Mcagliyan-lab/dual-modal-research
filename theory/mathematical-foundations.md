# 📐 Mathematical Foundations

## Notation and Definitions

### Network Structure
- $L$: Number of layers
- $\mathbf{A}^{(l)} \in \mathbb{R}^{B \times N^{(l)}}$: Activations at layer $l$
- $\mathbf{W}^{(l)} \in \mathbb{R}^{N^{(l)} \times N^{(l-1)}}$: Weight matrix between layers
- $N^{(l)}$: Number of neurons in layer $l$

### Temporal Analysis (NN-EEG)

#### Signal Extraction
$$s_t^{(l)} = \frac{1}{N^{(l)}} \sum_{i=1}^{N^{(l)}} |a_{i,t}^{(l)}|$$

#### Time Series Construction  
$$\mathbf{S}^{(l)} = [s_{t-W+1}^{(l)}, s_{t-W+2}^{(l)}, \ldots, s_t^{(l)}]$$

#### Power Spectral Density
$$P^{(l)}(f) = \frac{1}{K} \sum_{k=1}^K |F_k^{(l)}(f)|^2$$

where $F_k^{(l)}(f)$ is the FFT of the $k$-th window.

#### Frequency Band Power
$$\text{BP}_{\text{band}}^{(l)} = \sum_{f \in \text{band}} P^{(l)}(f)$$

#### State Classification Function
$$\text{State}^{(l)} = \arg\max_s \{\text{BP}_s^{(l)} : s \in \{\delta, \theta, \alpha, \beta, \gamma\}\}$$

### Spatial Analysis (NN-fMRI)

#### Grid Partitioning
$$\mathcal{G}^{(l)} = \{\mathcal{N}_{i,j,k} : i \in [g_h], j \in [g_w], k \in [g_c]\}$$

#### Spatial Density Function
$$\phi(g_{i,j,k}) = \frac{1}{|\mathcal{N}_{i,j,k}|} \sum_{(h,w,c) \in \mathcal{N}_{i,j,k}} |a_{h,w,c}^{(l)}| + \lambda \log(\sigma^2_{g_{i,j,k}} + \epsilon)$$

#### Impact Score (ζ-score)
$$\zeta(g) = \mathbb{E}_{S \subseteq \mathcal{G} \setminus \{g\}} [f(S \cup \{g\}) - f(S)]$$

#### Monte Carlo Approximation
$$\zeta(g) \approx \frac{1}{K} \sum_{k=1}^K [f(S_k \cup \{g\}) - f(S_k)]$$

#### Connection Strength
$$C_{A \rightarrow B} = \sum_{i \in A} \sum_{j \in B} |W_{ij}| \cdot \text{ReLU}(a_i) \cdot \sigma'(z_j)$$

### Cross-Modal Integration

#### Consistency Score
$$\text{Consistency}(t) = \frac{1}{3}[\rho_{\gamma\zeta}(t) + \text{Agreement}_{\text{state}}(t) + \text{Coherence}_{\text{anom}}(t)]$$

#### Temporal-Spatial Correlation
$$\rho_{\gamma\zeta}(t) = \text{corr}\left(\text{BP}_{\gamma}^{(l)}(t), \max_g \zeta_g^{(l)}(t)\right)$$

#### State Agreement Rate
$$\text{Agreement}_{\text{state}}(t) = \frac{1}{L} \sum_{l=1}^L \mathbb{I}[\text{State}_{\text{EEG}}^{(l)}(t) = \text{State}_{\text{fMRI}}^{(l)}(t)]$$

### Information Theory

#### Spectral Entropy
$$H_{\text{spectral}}^{(l)} = -\sum_f P^{(l)}(f) \log P^{(l)}(f)$$

#### Spatial Information Content
$$I_{\text{spatial}}(g) = H(Y) - H(Y|\phi(g))$$

#### Mutual Information Between Layers
$$I(L_i; L_j) = \sum_{f} P(f_{i,j}) \log \frac{P(f_{i,j})}{P(f_i)P(f_j)}$$

### Statistical Validation

#### Effect Size (Cohen's d)
$$d = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2 + s_2^2}{2}}}$$

#### Confidence Intervals (Bootstrap)
$$\text{CI}_{95\%} = [\text{percentile}_{2.5}, \text{percentile}_{97.5}]$$

#### Significance Testing
$$t = \frac{\bar{X} - \mu_0}{s/\sqrt{n}}$$

### Performance Metrics

#### Computational Complexity
- NN-EEG: $O(L \cdot W \cdot \log W)$ per analysis
- NN-fMRI: $O(L \cdot G \cdot K)$ per ζ-score calculation
- Integration: $O(L \cdot (W + G))$ per validation

#### Memory Requirements
- NN-EEG: $O(L \cdot W)$ for temporal buffers  
- NN-fMRI: $O(L \cdot G)$ for spatial grids
- Total: $O(L \cdot (W + G))$

### Theoretical Guarantees

#### Convergence Properties
For ζ-score estimation:
$$\mathbb{E}[\hat{\zeta}(g)] = \zeta(g)$$
$$\text{Var}[\hat{\zeta}(g)] = O(1/K)$$

#### Consistency Bounds
For cross-modal validation:
$$P(|\text{Consistency} - \text{True Consistency}| > \epsilon) \leq 2e^{-2n\epsilon^2}$$

### Implementation Considerations

#### Numerical Stability
- Add $\epsilon = 10^{-8}$ to prevent $\log(0)$
- Normalize PSD to prevent overflow
- Use double precision for accumulations

#### Optimization Strategies
- Vectorized operations for efficiency
- Sparse grid representation for memory
- Incremental PSD updates for real-time

### Validation Metrics

#### Reproducibility
$$\text{CV} = \frac{\sigma}{\mu}$$
Target: CV < 0.05 for excellent reproducibility

#### Cross-Modal Consistency
$$\text{Cohen's } \kappa = \frac{p_o - p_e}{1 - p_e}$$
Target: κ > 0.8 for strong agreement

#### Statistical Power
$$\text{Power} = P(\text{reject } H_0 | H_1 \text{ true})$$
Target: Power > 0.8 for adequate detection
