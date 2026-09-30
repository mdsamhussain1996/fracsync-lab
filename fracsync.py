# FracSync Lab: Chen system (lock) + linear feedback (key)
# Caputo derivative of order alpha, Adams-Bashforth-Moulton predictor-corrector (Diethelm, Ford, Freed).
# Needs numpy and matplotlib.
import numpy as np
import matplotlib.pyplot as plt
from math import gamma as Gamma

alpha, h, T = 0.95, 0.005, 15
lam = 1                 # projective factor: response follows lam * drive
feedforward = False        # add the compensation term lam*f(x) - f(y)?
tol = 0.01

# The lock: Chen system, D^alpha x = f(x)
a, b, c = 35, 3, 28
def f(x):
    return np.array([a*(x[1] - x[0]),
                     (c - a)*x[0] - x[0]*x[2] + c*x[1],
                     x[0]*x[1] - b*x[2]])
x0 = np.array([-3.0, 2.0, 20.0])   # drive initial state
y0 = np.array([-2.5, 2.5, 19.5])   # response initial state

# The key: linear feedback  u = -k e
k = 30
def control(e):
    return -k*e

# The solver: predictor x^P_{m+1} = x0 + sum_j wp[m+1-j] F_j,
#             corrector x_{m+1} = x0 + h^alpha/Gamma(alpha+2) * (F(x^P) + w0[m] F_0 + sum_j wc[m-j] F_j)
N = int(round(T/h))
g1, g2 = Gamma(alpha + 1), Gamma(alpha + 2)
kk = np.arange(N + 2, dtype=float)
wp = np.zeros(N + 2); wp[1:] = h**alpha/g1*(kk[1:]**alpha - (kk[1:] - 1)**alpha)
wc = (kk + 2)**(alpha + 1) + kk**(alpha + 1) - 2*(kk + 1)**(alpha + 1)
w0 = kk**(alpha + 1) - (kk - alpha)*(kk + 1)**alpha

n = len(x0)
X = np.zeros((N + 1, n)); Y = np.zeros((N + 1, n))
FX = np.zeros((N + 1, n)); FY = np.zeros((N + 1, n))    # F along the drive and along the controlled response
X[0], Y[0] = x0, y0
err = np.zeros(N + 1); err[0] = np.linalg.norm(Y[0] - lam*X[0])

for m in range(N):                             # step from t_m to t_(m+1)
    x, y = X[m], Y[m]
    fx, fy = f(x), f(y)
    e = y - lam*x
    u = control(e)
    if feedforward:
        u = u + lam*fx - fy                    # nonlinear compensation
    FX[m], FY[m] = fx, fy + u
    # predict
    xp = x0 + wp[m+1:0:-1] @ FX[:m+1]
    yp = y0 + wp[m+1:0:-1] @ FY[:m+1]
    # evaluate at the prediction
    fxp, fyp = f(xp), f(yp)
    up = control(yp - lam*xp)
    if feedforward:
        up = up + lam*fxp - fyp
    # correct
    rev = wc[:m][::-1]
    X[m+1] = x0 + h**alpha/g2*(fxp + w0[m]*FX[0] + rev @ FX[1:m+1])
    Y[m+1] = y0 + h**alpha/g2*(fyp + up + w0[m]*FY[0] + rev @ FY[1:m+1])
    err[m+1] = np.linalg.norm(Y[m+1] - lam*X[m+1])

above = np.where(err >= tol)[0]
if above.size == 0:
    settle = 0.0
elif above[-1] == N:
    settle = None
else:
    settle = float((above[-1] + 1)*h)
print("settling time:", settle, "| final error:", float(err[-1]))

t = np.arange(N + 1)*h
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
ax[0].semilogy(t, np.maximum(err, 1e-12)); ax[0].axhline(tol, ls="--", c="gray")
ax[0].set(xlabel="t", ylabel="||e(t)||", title="error")
ax[1].plot(t, X[:, 0], label="drive"); ax[1].plot(t, Y[:, 0], label="response")
ax[1].set(xlabel="t", title="first state"); ax[1].legend()
plt.tight_layout(); plt.show()
