"""
TMT-Net v13.0 — ТОЛЬКО ФИЗИКА
0 настроек. 1 закон: t = A
"""

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Данные — МЕНЯЙ ЗДЕСЬ ДЛЯ РАЗНЫХ ЗАДАЧ
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])  # XOR

# Начальные условия
np.random.seed(42)
w1 = np.random.randn(2, 8) * 0.5
b1 = np.zeros(8)
w2 = np.random.randn(8, 1) * 0.5
b2 = np.zeros(1)

# Единственная переменная
time = 0.0

print("="*60)
print("TMT-Net v13.0 — ТОЛЬКО t = A")
print("="*60)

for epoch in range(500):
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # ЗАКОН: время = действие
    time += (np.sum(np.abs(z1)) + np.sum(np.abs(z2))) / 8
    
    # ЗАКОН: скорость растёт от времени
    speed = min(4.0, 1.0 + time / 50)
    
    # Loss
    loss = np.mean(-y * np.log(a2 + 1e-8) - (1-y) * np.log(1-a2 + 1e-8))
    
    # Градиенты
    dz2 = a2 - y
    dw2 = (a1.T @ dz2) / 4
    db2 = np.sum(dz2, axis=0) / 4
    da1 = dz2 @ w2.T
    dz1 = da1 * (a1 * (1 - a1))
    dw1 = (X.T @ dz1) / 4
    db1 = np.sum(dz1, axis=0) / 4
    
    # Обновление — только скорость
    w2 -= speed * dw2
    b2 -= speed * db2
    w1 -= speed * dw1
    b1 -= speed * db1
    
    if epoch % 100 == 0:
        pred = (a2 > 0.5).astype(int).flatten()
        acc = (pred == y.flatten()).mean() * 100
        print(f"Эпоха {epoch:3d} | Loss: {loss:.6f} | Acc: {acc:.0f}% | Время: {time:.0f} | Скор: {speed:.2f}x")

# Результаты
print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ:")
print("="*60)
z1 = X @ w1 + b1
a1 = sigmoid(z1)
z2 = a1 @ w2 + b2
a2 = sigmoid(z2)
pred = (a2 > 0.5).astype(int).flatten()
for i in range(4):
    print(f"  {'✅' if pred[i]==y[i][0] else '❌'} {X[i][0]} ⊕ {X[i][1]} = {pred[i]}")
print(f"\nТочность: {(pred == y.flatten()).mean() * 100:.0f}%")
print(f"Всего времени: {time:.0f}")
print("\n0 НАСТРОЕК. ТОЛЬКО t = A.")
print("="*60)
input("\nНажми Enter...")
