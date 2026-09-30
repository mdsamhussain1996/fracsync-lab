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
- **The Lock:** The driving nonlinear dynamical network (chaotic attractor or neural network).
- **The Key:** The control law applied to the response system, whose teeth heights correspond directly to controller gains.
- **The Turn:** Turning the key simulates the coupled system over time via the **Grünwald–Letnikov scheme** for the Caputo fractional derivative. If the synchronization error $\|e(t)\|$ decays below tolerance ($\varepsilon = 0.01$), the padlock opens; if gains are insufficient or diverge, the lock jams.

---

## 🔬 Theoretical Foundations

### 1. Caputo Fractional Derivative
For fractional order $\alpha \in (0, 1]$, the Caputo derivative of a state $x(t)$ with starting time $t_0=0$ is defined as:
$${}^C\!D^\alpha x(t) = \frac{1}{\Gamma(1 - \alpha)} \int_0^t (t - \tau)^{-\alpha} x'(\tau) \, d\tau$$

### 2. Grünwald–Letnikov Numerical Integration
The simulator integrates the memory of the fractional derivative using the discretized Grünwald–Letnikov approximation with time step $h = 0.005$:
$$x_m = x_0 + h^\alpha F(x_{m-1}) - \sum_{j=1}^{m} c_j \left(x_{m-j} - x_0\right)$$
where the memory weights $c_j$ satisfy the recurrence relation:
$$c_0 = 1, \quad c_j = \left(1 - \frac{1 + \alpha}{j}\right) c_{j-1}$$

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

## 🧩 Supported Systems (The Locks)

| System | State Dimension | Description | Attractor / Characteristics |
| :--- | :---: | :--- | :--- |
| **Chen System** | $n = 3$ | Classic chaotic attractor discovered by G. Chen (1999) | Dual-scroll chaotic attractor with parameters $a=35, b=3, c=28$ |
| **Hopfield Network** | $n = 3$ | Coupled nonlinear neural network with $\tanh(\cdot)$ activations | 3-neuron network with weight matrix $W \in \mathbb{R}^{3 \times 3}$ |
| **Quaternion Network** | $n = 8$ | Quaternion-valued neural network in $\mathbb{H}$ | 2 neurons in $\mathbb{H}$ ($q = q_0 + q_1 i + q_2 j + q_3 k$) with non-commutative Hamilton product |

---

## 🔑 Supported Controllers (The Keys)

1. **Linear Feedback Controller**:
   $$u(t) = -k\,e(t)$$
   Decays via Mittag-Leffler algebraic behavior for fractional systems.
2. **Fixed-Time Controller**:
   $$u_i(t) = -k_1 \operatorname{sig}(e_i)^{p} - k_2 \operatorname{sig}(e_i)^{q}, \quad 0 < p < 1 < q$$
   Guarantees fast convergence near zero ($p$-term) and far from the origin ($q$-term).
3. **Sliding Mode Controller (Smooth Boundary Layer)**:
   $$u(t) = -k\,e(t) - \eta \tanh\left(\frac{e(t)}{\varepsilon}\right)$$
   Smooth tanh approximation eliminates high-frequency chattering.
4. **Adaptive Gain Controller**:
   $$u(t) = -\kappa(t)\,e(t), \quad \dot{\kappa}(t) = \gamma \|e(t)\|^2, \quad \kappa(0) = \kappa_0$$
   Controller teeth automatically grow until synchronization is achieved.
5. **Impulsive Controller**:
   $$e(t_m^+) = (1 - \mu) e(t_m^-) \quad \text{at } t_m = m\Delta$$
   Instantaneous discrete resets without continuous actuation between impulses.

---

## 🚀 Live Demo & Usage

### 🌐 Browser (Zero Setup)
Visit the live laboratory: **[https://mdsamhussain1996.github.io/fracsync-lab/](https://mdsamhussain1996.github.io/fracsync-lab/)**

Or open [`index.html`](index.html) locally in any browser (Chrome, Safari, Firefox, Edge). No build tools, package managers, or servers required.

### 🐍 Python Simulation Engine
You can also run the companion Python engine directly from the command line:

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
├── index.html         # Complete interactive simulator (Lock & Key bench + Canvas plots)
├── fracsync.py        # Standalone, reproducible Python simulation CLI
├── README.md          # Full documentation & mathematical derivations
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

If you use **FracSync Lab** in your research, teaching, or presentations, please cite:

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
