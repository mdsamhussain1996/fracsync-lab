# FracSync Lab 🔐

**Interactive Laboratory for Drive–Response Synchronization of Fractional-Order Chaotic Networks and Neural Systems**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-2D4FA1?style=for-the-badge&logo=github)](https://mdsamhussain1996.github.io/fracsync-lab/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Vanilla JS](https://img.shields.io/badge/Zero%20Dependencies-HTML%2FCSS%2FJS-E2A83B?style=for-the-badge)](index.html)
[![Python Engine](https://img.shields.io/badge/Python-NumPy%20%7C%20Matplotlib-1E8A4B?style=for-the-badge&logo=python)](fracsync.py)

---

## 🧭 Overview

> *"Every chaotic network is a lock. Every controller is a key. Cut a key, turn it, and see whether the response system falls into step with the drive."*

**FracSync Lab** is an interactive, browser-native research and visualization laboratory designed for exploring **drive–response synchronization in fractional-order nonlinear dynamical systems**. It models the synchronization problem through the tangible metaphor of a locksmith’s bench:
- **The Lock:** The driving nonlinear dynamical network (chaotic attractor or neural network). Grouped under three families:
  1. **Family A:** 3D & 4D Chaotic Attractors (Chen, Lorenz, Lü, Rössler, Chua, Liu, Genesio-Tesi, Hyperchaotic Chen).
  2. **Family B:** Real-Valued Neural Networks (Hopfield, Competitive, Cohen-Grossberg, BAM, CNN).
  3. **Family C:** Quaternion-Valued Neural Networks in $\mathbb{H}$ (Quaternion network, Q-Hopfield, Q-Cohen-Grossberg, Q-BAM, Q-CNN).
- **The Key:** The control law applied to the response system, whose teeth heights correspond directly to controller gains (Linear feedback, Fixed-time, Sliding mode, Adaptive gain, Impulsive control).
- **The Turn:** Turning the key simulates the coupled system over time via the **Adams–Bashforth–Moulton predictor–corrector scheme** (Diethelm, Ford, Freed) for the Caputo fractional derivative. If the synchronization error $\|e(t)\|$ decays below tolerance ($\varepsilon = 0.01$), the padlock opens; if gains are insufficient or diverge, the lock jams.

---

## 🔬 Theoretical Foundations

### 1. Caputo Fractional Derivative
For fractional order $\alpha \in (0, 1]$, the Caputo derivative of a state $x(t)$ with starting time $t_0=0$ is defined as:
$${}^C\!D^\alpha x(t) = \frac{1}{\Gamma(1 - \alpha)} \int_0^t (t - \tau)^{-\alpha} x'(\tau) \, d\tau$$

### 2. Adams–Bashforth–Moulton (ABM) Predictor–Corrector Numerical Integration
The simulator implements the predictor–corrector scheme by Kai Diethelm, Neville J. Ford, and Alan D. Freed (2002), which achieves $O(h^{\min(2, 1+\alpha)})$ accuracy for the Caputo fractional derivative:

**Predictor (Adams–Bashforth step):**
$$x_{m+1}^P = x_0 + \sum_{j=0}^{m} w_{m+1-j}^p F(x_j), \quad w_k^p = \frac{h^\alpha}{\Gamma(\alpha + 1)} \left[ k^\alpha - (k-1)^\alpha \right]$$

**Corrector (Adams–Moulton step):**
$$x_{m+1} = x_0 + \frac{h^\alpha}{\Gamma(\alpha + 2)} \left[ F(x_{m+1}^P) + w_0(m) F(x_0) + \sum_{j=1}^{m} w_{m-j}^c F(x_j) \right]$$
where the corrector weights are:
$$w_k^c = (k + 2)^{\alpha + 1} + k^{\alpha + 1} - 2(k + 1)^{\alpha + 1}, \quad w_0(m) = m^{\alpha + 1} - (m - \alpha)(m + 1)^\alpha$$

### 3. Drive–Response Synchronization
Let the drive system be:
$${}^C\!D^\alpha x(t) = f(x(t))$$
and the response system under controller $u(t)$ be:
$${}^C\!D^\alpha y(t) = f(y(t)) + u(t)$$
Defining the projective synchronization error $e(t) = y(t) - \lambda x(t)$, where $\lambda \in \mathbb{R}$ is the projective scaling factor:
$${}^C\!D^\alpha e(t) = f(y(t)) - \lambda f(x(t)) + u(t)$$
When nonlinear compensation (feedforward) is enabled:
$$u(t) = v(e(t)) + \lambda f(x(t)) - f(y(t)) \implies {}^C\!D^\alpha e(t) = v(e(t))$$

---

## 🧩 Supported Systems (18 Locks across 3 Families)

### Family A: Chaotic Systems (3D & 4D Real Attractors)
| System | Dim | Parameters & Attractor | Chaos Condition |
| :--- | :---: | :--- | :--- |
| **Chen System** | $n=3$ | $a=35, b=3, c=28$; dual-scroll attractor | $\alpha \ge 0.83$ |
| **Lorenz System** | $n=3$ | $\sigma=10, \rho=28, \beta=8/3$; butterfly attractor | $\alpha \ge 0.985$ (default $\alpha=0.99$) |
| **Lü System** | $n=3$ | $a=36, b=3, c=20$; bridges Lorenz and Chen systems | $\alpha \ge 0.80$ |
| **Rössler System** | $n=3$ | $a=0.2, b=0.2, c=5.7$; folded band attractor | $\alpha \ge 0.90$ |
| **Chua Circuit** | $n=3$ | $\alpha_c=10, \beta_c=14.87$; piecewise-linear diode | $\alpha \ge 0.93$ |
| **Liu System** | $n=3$ | $a=10, b=40, c=2.5, d=4$; squared nonlinear feedback | $\alpha \ge 0.85$ |
| **Genesio-Tesi System** | $n=3$ | $a=1.2, b=2.92, c=6$; polynomial quadratic chaos | $\alpha \ge 0.92$ |
| **Hyperchaotic Chen** | $n=4$ | 4D hyperchaos with 2 positive Lyapunov exponents | $\alpha \ge 0.90$ |

### Family B: Real-Valued Neural Networks
| System | Dim | Equations & Matrices | Dynamics |
| :--- | :---: | :--- | :--- |
| **Hopfield Network** | $n=3$ | ${}^C D^\alpha x = -x + W \tanh(x)$; asymmetric weight matrix $W$ | Chaotic limit cycles |
| **Competitive Network** | $n=3$ | Self-excitation ($W_{ii}>0$), mutual lateral inhibition ($W_{ij}<0$) | Multi-stable competitive memory |
| **Cohen-Grossberg Network** | $n=3$ | Non-Lipschitz amplification $a_i(x)=1+0.2\cos(x)$, $b_i(x)=1.2x$ | Non-constant amplification dynamics |
| **BAM Network** | $n=4$ | Bidirectional memory: ${}^C D^\alpha x = -x + P \tanh(y)$, ${}^C D^\alpha y = -y + Q \tanh(x)$ | Inter-layer oscillatory resonance |
| **Cellular Network (CNN)** | $n=3$ | Nearest-neighbor cloning template matrix $A$ with constant cell bias | Spatial pattern oscillations |

### Family C: Quaternion-Valued Neural Networks ($\mathbb{H}$, 8D Real States)
All models use the non-commutative Hamilton product $\otimes$ and componentwise split activations:
| System | Real Dim | Quaternion Description |
| :--- | :---: | :--- |
| **Quaternion Network** | $n=8$ | 2 neurons in $\mathbb{H}$ coupled by quaternion weight matrix $A \in \mathbb{H}^{2 \times 2}$ |
| **Quaternion Hopfield** | $n=8$ | 2 quaternion neurons with asymmetric quaternion couplings $W \in \mathbb{H}^{2 \times 2}$ |
| **Quaternion Cohen-Grossberg** | $n=8$ | Componentwise state-dependent amplification $a(z) = 1 + 0.15\cos(z)$ per real channel |
| **Quaternion BAM** | $n=8$ | 2 quaternion layers: forward coupling $P \in \mathbb{H}$, backward coupling $Q \in \mathbb{H}$ |
| **Quaternion CNN** | $n=8$ | 2 quaternion cells coupled via spatial template $A \in \mathbb{H}^{2 \times 2}$ with bias vectors |

---

## 🔑 Supported Controllers (The 5 Keys)

1. **Linear Feedback Controller**:
   $$u(t) = -k\,e(t)$$
2. **Fixed-Time Controller**:
   $$u_i(t) = -k_1 \operatorname{sig}(e_i)^{p} - k_2 \operatorname{sig}(e_i)^{q}, \quad 0 < p < 1 < q$$
3. **Sliding Mode Controller (Smooth Boundary Layer)**:
   $$u(t) = -k\,e(t) - \eta \tanh\left(\frac{e(t)}{\varepsilon}\right)$$
4. **Adaptive Gain Controller**:
   $$u(t) = -\kappa(t)\,e(t), \quad \dot{\kappa}(t) = \gamma \|e(t)\|^2, \quad \kappa(0) = \kappa_0$$
5. **Impulsive Controller**:
   $$e(t_m^+) = (1 - \mu) e(t_m^-) \quad \text{at } t_m = m\Delta$$

---

## ⏱️ Time & Step Controls & Web Worker Engine

- **Time Span $T$:** Presets for $5$, $15$, $30$, $60$, $100$ s + arbitrary custom input.
- **Step Size $h$:** Presets for $0.01$, $0.005$, and $0.0025$ s.
- **Cost Scaling Indicator:** Computes step count $N = \text{round}(T/h)$ and automatically flags long runs ($N > 8,000$ steps) where $O(N^2)$ ABM memory requires high compute.
- **Background Web Worker:** High-step simulations ($N > 3,000$) run asynchronously in an inline Web Worker (created via Blob URL) with an active progress bar and a **Cancel** button, ensuring the main browser thread remains 100% responsive.
- **Plot Downsampling:** Canvas plots automatically downsample trajectories to $\le 2,000$ points for smooth 60 FPS rendering.

---

## 🚀 Live Demo & Usage

### 🌐 Browser (Zero Setup)
Visit the live laboratory: **[https://mdsamhussain1996.github.io/fracsync-lab/](https://mdsamhussain1996.github.io/fracsync-lab/)**

Or open [`index.html`](index.html) or [`fracsync-lab.html`](fracsync-lab.html) locally in any browser (Chrome, Safari, Firefox, Edge).

### 🐍 Python Simulation Engine
```bash
# Clone the repository
git clone https://github.com/mdsamhussain1996/fracsync-lab.git
cd fracsync-lab

# Install dependencies (NumPy & Matplotlib)
pip install numpy matplotlib

# Run default simulation (Chen system with Linear control)
python3 fracsync.py

# Run Quaternion-valued neural network with Fixed-Time control
python3 fracsync.py --system quat --control fixedtime --alpha 0.95 --feedforward

# Run Hopfield network with Sliding Mode control
python3 fracsync.py --system hopfield --control sliding --alpha 0.92
```

---

## 📂 Repository Structure

```
fracsync-lab/
├── index.html         # Main GitHub Pages entry point (interactive workbench + Web Worker)
├── fracsync-lab.html  # Standalone single-file interactive simulator
├── fracsync.py        # Standalone Python simulation CLI
├── README.md          # Full documentation, mathematical models & verification matrix
└── LICENSE            # MIT License
```

---

## 👨‍🏫 Author & Citation

**Dr. Md Samshad Hussain Ansari**  
*Assistant Professor (Mathematics)*  
Newton School of Technology, ADYPU, Pune  
Ph.D. in Mathematics, Indian Institute of Technology (IIT) Mandi (2021–2025)  
Research Focus: Synchronization of fractional-order quaternion-valued dynamical systems & neural networks  
Website: [https://mdsamhussain1996.github.io/](https://mdsamhussain1996.github.io/)

```bibtex
@misc{ansari2026fracsync,
  author = {Ansari, Md Samshad Hussain},
  title = {FracSync Lab: Interactive Laboratory for Drive-Response Synchronization of Fractional-Order Networks},
  year = {2026},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/mdsamhussain1996/fracsync-lab}}
}
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
