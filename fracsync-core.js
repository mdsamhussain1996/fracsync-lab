// fracsync-core.js
// ─────────────────────────────────────────────────────────────────────────────
// Shared numerical routines for FracSync Lab & Research Demos
// Adams–Bashforth–Moulton (ABM) predictor–corrector scheme for Caputo fractional-order systems
// (Diethelm, Ford, Freed, 2002) with quaternion algebra (Hamilton product).
// ─────────────────────────────────────────────────────────────────────────────

(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.FracSyncCore = factory();
  }
}(typeof self !== 'undefined' ? self : this, function() {
  'use strict';

  // ── 1. Hamilton Quaternion Multiplication (a * b)
  // Quaternions represented as 4-element arrays [Re, i, j, k]
  function qmul(a, b) {
    return [
      a[0]*b[0] - a[1]*b[1] - a[2]*b[2] - a[3]*b[3],
      a[0]*b[1] + a[1]*b[0] + a[2]*b[3] - a[3]*b[2],
      a[0]*b[2] - a[1]*b[3] + a[2]*b[0] + a[3]*b[1],
      a[0]*b[3] + a[1]*b[2] - a[2]*b[1] + a[3]*b[0]
    ];
  }

  // ── 2. Quaternion Norm & Conjugate
  function qnorm(q) {
    return Math.sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3]);
  }
  function qconj(q) {
    return [q[0], -q[1], -q[2], -q[3]];
  }

  // ── 3. Lanczos Gamma Function Approximation
  function gamma(z) {
    const g = 7;
    const C = [
      0.99999999999980993,
      676.5203681218851,
      -1259.1392167224028,
      771.32342877765313,
      -176.61502916214059,
      12.507343278686905,
      -0.138571095836526,
      9.9843695780195716e-6,
      1.5056327351493116e-7
    ];
    if (z < 0.5) return Math.PI / (Math.sin(Math.PI * z) * gamma(1 - z));
    z -= 1;
    let x = C[0];
    for (let i = 1; i < g + 2; i++) x += C[i] / (z + i);
    const t = z + g + 0.5;
    return Math.sqrt(2 * Math.PI) * Math.pow(t, z + 0.5) * Math.exp(-t) * x;
  }

  // ── 4. Precompute ABM Predictor-Corrector Weights
  function abmWeights(N, alpha, h) {
    const g1 = gamma(alpha + 1);
    const g2 = gamma(alpha + 2);
    const hal = Math.pow(h, alpha);
    const invG2 = hal / g2;

    const wp = new Float64Array(N + 2);
    const wc = new Float64Array(N + 2);
    const w0 = new Float64Array(N + 2);

    for (let j = 0; j <= N + 1; j++) {
      if (j > 0) wp[j] = (hal / g1) * (Math.pow(j, alpha) - Math.pow(j - 1, alpha));
      wc[j] = Math.pow(j + 2, alpha + 1) + Math.pow(j, alpha + 1) - 2 * Math.pow(j + 1, alpha + 1);
      w0[j] = Math.pow(j, alpha + 1) - (j - alpha) * Math.pow(j + 1, alpha);
    }

    return { wp, wc, w0, invG2, hal };
  }

  // ── 5. Vector Utility Functions
  function norm(vec) {
    let s = 0;
    for (let i = 0; i < vec.length; i++) s += vec[i] * vec[i];
    return Math.sqrt(s);
  }

  function errorNorm(y, x, lam = 1) {
    let s = 0;
    for (let i = 0; i < y.length; i++) {
      const diff = y[i] - lam * x[i];
      s += diff * diff;
    }
    return Math.sqrt(s);
  }

  // ── 6. Numerical Statistics & Settling Time
  function computeStats(err, h, tol = 0.01, diverged = null) {
    const N = err.length - 1;
    let last = -1;
    let peak = 0;
    for (let k = 0; k <= N; k++) {
      if (err[k] >= tol) last = k;
      if (err[k] > peak) peak = err[k];
    }
    const settle = (diverged !== null || last === N) ? null : (last + 1) * h;
    return {
      settle,
      final: err[N],
      peak,
      open: settle !== null
    };
  }

  // ── 7. Downsampling for High-Speed Canvas Rendering
  function downsampleSeries(tArr, valArr, maxPoints = 2000) {
    const len = tArr.length;
    if (len <= maxPoints) return { t: tArr, y: valArr };
    const step = Math.ceil(len / maxPoints);
    const subT = [];
    const subY = [];
    for (let i = 0; i < len; i += step) {
      subT.push(tArr[i]);
      subY.push(valArr[i]);
    }
    if (subT[subT.length - 1] !== tArr[len - 1]) {
      subT.push(tArr[len - 1]);
      subY.push(valArr[len - 1]);
    }
    return { t: subT, y: subY };
  }

  return {
    qmul,
    qnorm,
    qconj,
    gamma,
    abmWeights,
    norm,
    errorNorm,
    computeStats,
    downsampleSeries
  };
}));
