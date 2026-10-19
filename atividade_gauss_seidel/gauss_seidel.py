import numpy as np
import matplotlib.pyplot as plt

A = np.array([[10.0, -1.0, 2.0],
              [-1.0, 11.0, -1.0],
              [2.0, -1.0, 10.0]])
b = np.array([6.0, 22.0, -10.0])


def gauss_seidel(A, b, x0, tol=1e-5, max_iter=100):
    n = len(b)
    x = x0.astype(float).copy()
    history = [x.copy()]
    errors = [np.nan]
    for k in range(1, max_iter + 1):
        x_old = x.copy()
        for i in range(n):
            s = A[i, :i] @ x[:i] + A[i, i + 1:] @ x_old[i + 1:]
            x[i] = (b[i] - s) / A[i, i]
        error = np.max(np.abs(x - x_old))
        history.append(x.copy())
        errors.append(error)
        if error < tol:
            return x, k, np.array(history), np.array(errors)
    return x, max_iter, np.array(history), np.array(errors)


x0 = np.zeros(3)
solution, iterations, history, errors = gauss_seidel(A, b, x0)

print(f"Iterações realizadas: {iterations}")
print(f"Solução aproximada: x = {solution[0]:.6f}, y = {solution[1]:.6f}, z = {solution[2]:.6f}")
print()
print(f"{'k':>3} | {'x(k)':>10} | {'y(k)':>10} | {'z(k)':>10} | {'||x(k)-x(k-1)||inf':>20}")
print("-" * 66)
for k, (xk, ek) in enumerate(zip(history, errors)):
    err = "-" if np.isnan(ek) else f"{ek:.6e}"
    print(f"{k:>3} | {xk[0]:>10.6f} | {xk[1]:>10.6f} | {xk[2]:>10.6f} | {err:>20}")

k_values = np.arange(len(history))

plt.figure(figsize=(8, 5))
plt.plot(k_values, history[:, 0], "o-", label="$x^{(k)}$")
plt.plot(k_values, history[:, 1], "s-", label="$y^{(k)}$")
plt.plot(k_values, history[:, 2], "^-", label="$z^{(k)}$")
plt.xlabel("Iteração $k$")
plt.ylabel("Valor")
plt.title("Evolução das aproximações (Gauss–Seidel)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("grafico_aproximacoes.png", dpi=150)
plt.show()

plt.figure(figsize=(8, 5))
plt.semilogy(k_values[1:], errors[1:], "o-", color="tab:red")
plt.axhline(1e-5, color="gray", linestyle="--", label="tolerância $10^{-5}$")
plt.xlabel("Iteração $k$")
plt.ylabel(r"$\|\mathbf{x}^{(k)}-\mathbf{x}^{(k-1)}\|_\infty$")
plt.title("Erro entre iterações (escala logarítmica)")
plt.grid(True, which="both", alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("grafico_erro.png", dpi=150)
plt.show()
