#!/usr/bin/env python3
"""
FracSync Lab: Fractional-Order Network Synchronization
Author: Dr. Md Samshad Hussain Ansari (Newton School of Technology, ADYPU / PhD IIT Mandi)
Repository: https://github.com/mdsamhussain1996/fracsync-lab

Solves drive-response synchronization for fractional-order chaotic and neural networks
using the Grünwald-Letnikov discretization of the Caputo fractional derivative:
  {}^C D^alpha x(t) = f(x(t))
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# System Definitions (The Locks)
# -------------------------------------------------------------

CH_PARAMS = {'a': 35.0, 'b': 3.0, 'c': 28.0}
HW_WEIGHTS = np.array([
    [2.0, -1.2, 0.0],
    [1.9995, 1.71, 1.15],
    [0.0, -4.75, 1.1]
])
QP_D = 1.0
QP_A = [
    [np.array([2.0, -0.5, 0.3, 0.0]), np.array([-1.5, 1.0, 0.0, 0.5])],
    [np.array([1.8, 0.4, -0.6, 0.2]), np.array([1.6, -0.7, 0.5, -0.3])]
]

def qmul(p, q):
    """Hamilton product of two quaternions in R^4."""
    return np.array([
        p[0]*q[0] - p[1]*q[1] - p[2]*q[2] - p[3]*q[3],
        p[0]*q[1] + p[1]*q[0] + p[2]*q[3] - p[3]*q[2],
        p[0]*q[2] - p[1]*q[3] + p[2]*q[0] + p[3]*q[1],
        p[0]*q[3] + p[1]*q[2] - p[2]*q[1] + p[3]*q[0]
    ])

def f_chen(x):
    a, b, c = CH_PARAMS['a'], CH_PARAMS['b'], CH_PARAMS['c']
    return np.array([
        a * (x[1] - x[0]),
        (c - a) * x[0] - x[0] * x[2] + c * x[1],
        x[0] * x[1] - b * x[2]
    ])

def f_hopfield(x):
    return -x + HW_WEIGHTS @ np.tanh(x)

def f_quat(x):
    t = np.tanh(x).reshape(2, 4)
    out = []
    for i in range(2):
        s = sum(qmul(QP_A[i][j], t[j]) for j in range(2))
        out.append(-QP_D * x[4*i:4*i+4] + s)
    return np.concatenate(out)

SYSTEMS = {
    'chen': {
        'name': 'Chen System (3D Chaotic Attractor)',
        'f': f_chen,
        'x0': np.array([-3.0, 2.0, 20.0]),
        'y0': np.array([4.0, -6.0, 12.0]),
        'proj': (0, 2),
        'labels': ('x1', 'x3')
    },
    'hopfield': {
        'name': 'Hopfield Neural Network (3 Neurons)',
        'f': f_hopfield,
        'x0': np.array([0.2, 0.1, -0.1]),
        'y0': np.array([-0.3, 0.4, 0.2]),
        'proj': (0, 1),
        'labels': ('x1', 'x2')
    },
    'quat': {
        'name': 'Quaternion-Valued Network (2 Neurons in H, 8 States)',
        'f': f_quat,
        'x0': np.array([0.3, -0.2, 0.1, 0.4, -0.1, 0.2, 0.3, -0.3]),
        'y0': np.array([-0.4, 0.3, -0.2, 0.1, 0.3, -0.3, 0.1, 0.2]),
        'proj': (0, 1),
        'labels': ('Re(q1)', 'i-part(q1)')
    }
}

# -------------------------------------------------------------
# Simulation Engine
# -------------------------------------------------------------

def simulate(sys_name='chen', ctrl_type='linear', alpha=0.95, h=0.005, T=15.0,
             feedforward=False, lam=1.0, tol=0.01, **gains):
    sys_cfg = SYSTEMS[sys_name]
    f = sys_cfg['f']
    x0, y0 = sys_cfg['x0'].copy(), sys_cfg['y0'].copy()
    n = len(x0)
    N = int(round(T / h))

    # Grünwald-Letnikov weights c_j for fractional order alpha
    gl = np.ones(N + 1)
    for j in range(1, N + 1):
        gl[j] = (1.0 - (1.0 + alpha) / j) * gl[j - 1]

    X = np.zeros((N + 1, n))
    Y = np.zeros((N + 1, n))
    err = np.zeros(N + 1)

    X[0] = x0
    Y[0] = y0
    err[0] = np.linalg.norm(Y[0] - lam * X[0])

    # Default gains if not passed
    is_chen = (sys_name == 'chen')
    k = gains.get('k', 30.0 if is_chen else 2.0)
    k1 = gains.get('k1', 10.0 if is_chen else 2.0)
    k2 = gains.get('k2', 2.0 if is_chen else 1.0)
    p = gains.get('p', 0.5)
    q = gains.get('q', 1.5)
    eta = gains.get('eta', 10.0 if is_chen else 1.0)
    eps = gains.get('eps', 0.1)
    kappa = gains.get('k0', 1.0 if is_chen else 0.1)
    gamma = gains.get('gamma', 20.0 if is_chen else 5.0)
    dt_imp = gains.get('dt', 0.02 if is_chen else 0.1)
    mu = gains.get('mu', 0.6 if is_chen else 0.5)

    every = max(1, int(round(dt_imp / h))) if ctrl_type == 'impulsive' else 0

    for m in range(1, N + 1):
        x = X[m - 1]
        y = Y[m - 1]
        fx = f(x)
        fy = f(y)
        e = y - lam * x

        # Compute control law u
        if ctrl_type == 'linear':
            u = -k * e
        elif ctrl_type == 'fixedtime':
            sig_p = np.sign(e) * (np.abs(e) ** p)
            sig_q = np.sign(e) * (np.abs(e) ** q)
            u = -k1 * sig_p - k2 * sig_q
        elif ctrl_type == 'sliding':
            u = -k * e - eta * np.tanh(e / eps)
        elif ctrl_type == 'adaptive':
            u = -kappa * e
            kappa += h * gamma * np.dot(e, e)
        elif ctrl_type == 'impulsive':
            u = np.zeros_like(e)
        else:
            raise ValueError(f"Unknown control type: {ctrl_type}")

        if feedforward:
            u = u + lam * fx - fy

        # Caputo fractional memory summation
        memx = np.tensordot(gl[1:m + 1], X[m - 1::-1] - x0, axes=1)
        memy = np.tensordot(gl[1:m + 1], Y[m - 1::-1] - y0, axes=1)

        X[m] = x0 + (h ** alpha) * fx - memx
        Y[m] = y0 + (h ** alpha) * (fy + u) - memy

        if every and (m % every == 0):
            Y[m] -= mu * (Y[m] - lam * X[m])

        err[m] = np.linalg.norm(Y[m] - lam * X[m])
        if not np.isfinite(err[m]) or err[m] > 1e6:
            print(f"Warning: numerical blowup at step m={m}, t={m*h:.2f}s")
            err[m:] = err[m - 1]
            X[m:] = X[m - 1]
            Y[m:] = Y[m - 1]
            break

    # Settling time determination
    above = np.where(err >= tol)[0]
    settle = None if (above.size > 0 and above[-1] == N) else (0.0 if above.size == 0 else float((above[-1] + 1) * h))

    return {
        't': np.arange(N + 1) * h,
        'X': X,
        'Y': Y,
        'err': err,
        'settle': settle,
        'final_err': float(err[-1]),
        'peak_err': float(np.max(err)),
        'sys_cfg': sys_cfg
    }

def main():
    parser = argparse.ArgumentParser(description="FracSync Lab Simulation Engine")
    parser.add_argument('--system', choices=['chen', 'hopfield', 'quat'], default='chen', help="Dynamical network model")
    parser.add_argument('--control', choices=['linear', 'fixedtime', 'sliding', 'adaptive', 'impulsive'], default='linear', help="Controller type")
    parser.add_argument('--alpha', type=float, default=0.95, help="Caputo fractional derivative order")
    parser.add_argument('--h', type=float, default=0.005, help="Integration step size")
    parser.add_argument('--T', type=float, default=15.0, help="Simulation duration (s)")
    parser.add_argument('--feedforward', action='store_true', help="Compensate nonlinear terms")
    parser.add_argument('--lambda_factor', type=float, default=1.0, help="Projective synchronization scaling factor")
    parser.add_argument('--tol', type=float, default=0.01, help="Convergence tolerance")
    parser.add_argument('--no-plot', action='store_true', help="Disable matplotlib visual display")

    args = parser.parse_args()

    print(f"--- Running FracSync Simulation ---")
    print(f"System: {args.system} | Controller: {args.control} | alpha: {args.alpha}")

    res = simulate(
        sys_name=args.system,
        ctrl_type=args.control,
        alpha=args.alpha,
        h=args.h,
        T=args.T,
        feedforward=args.feedforward,
        lam=args.lambda_factor,
        tol=args.tol
    )

    settle_str = f"{res['settle']:.2f} s" if res['settle'] is not None else "Not reached"
    print(f"Settling Time: {settle_str}")
    print(f"Final Error:   {res['final_err']:.4e}")
    print(f"Peak Error:    {res['peak_err']:.4f}")

    if not args.no_plot:
        t = res['t']
        cfg = res['sys_cfg']
        p0, p1 = cfg['proj']
        l0, l1 = cfg['labels']

        fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))

        # Error norm plot
        ax[0].semilogy(t, np.maximum(res['err'], 1e-12), 'k-', lw=1.5, label=r'$\|e(t)\|$')
        ax[0].axhline(args.tol, ls='--', color='green', lw=1.2, label=f'Tol ({args.tol})')
        if res['settle'] is not None:
            ax[0].axvline(res['settle'], ls=':', color='green', label=f'Settled: {res["settle"]:.2f}s')
        ax[0].set(xlabel='Time $t$ (s)', ylabel='Error Norm $\|e(t)\|$', title='Synchronization Error')
        ax[0].grid(True, alpha=0.3)
        ax[0].legend()

        # First state trajectory
        ax[1].plot(t, res['X'][:, 0], 'b-', lw=1.4, label='Drive $x_1(t)$')
        ax[1].plot(t, res['Y'][:, 0], 'r--', lw=1.4, label='Response $y_1(t)$')
        ax[1].set(xlabel='Time $t$ (s)', ylabel='State amplitude', title='First State Dynamics')
        ax[1].grid(True, alpha=0.3)
        ax[1].legend()

        # Phase portrait
        ax[2].plot(res['X'][:, p0], res['X'][:, p1], 'b-', lw=1.0, alpha=0.8, label='Drive Attractor')
        ax[2].plot(res['Y'][:, p0], res['Y'][:, p1], 'r--', lw=1.0, alpha=0.8, label='Response Trajectory')
        ax[2].set(xlabel=l0, ylabel=l1, title=f'Phase Portrait ({l0} vs {l1})')
        ax[2].grid(True, alpha=0.3)
        ax[2].legend()

        plt.suptitle(f"FracSync Lab — {cfg['name']} under {args.control.capitalize()} Control ($\\alpha={args.alpha}$)", fontsize=12)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    main()
