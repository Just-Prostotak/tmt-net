"""
TMT-Net v10.0 - ЧИСТАЯ БЫСТРАЯ ВЕРСИЯ
Время со ВСЕХ слоев, глобальное накопление
"""

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_deriv(x):
    return x * (1 - x)

# Данные
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

# Инициализация
np.random.seed(42)
w1 = np.random.randn(2, 8) * 0.5
b1 = np.zeros(8)
w2 = np.random.randn(8, 1) * 0.5
b2 = np.zeros(1)

# Глобальное время (НЕ СБРАСЫВАЕМ!)
global_time = 0.0
base_lr = 0.6

print("="*60)
print("TMT-Net v10.0 - ЧИСТАЯ БЫСТРАЯ ВЕРСИЯ")
print("Время со всех слоев, глобальное накопление")
print("="*60)

for epoch in range(300):
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # TMT: накапливаем время со ВСЕХ слоев
    epoch_time = (np.sum(np.abs(z1)) + np.sum(np.abs(z2))) / 8
    global_time += epoch_time
    
    # Скорость: время ускоряет
    speed = 1 + min(3.0, global_time / 50)
    current_lr = base_lr * speed
    
    # Loss
    loss = np.mean(-y * np.log(a2 + 1e-8) - (1-y) * np.log(1-a2 + 1e-8))
    
    # Backward
    dz2 = a2 - y
    dw2 = (a1.T @ dz2) / 4
    db2 = np.sum(dz2, axis=0) / 4
    da1 = dz2 @ w2.T
    dz1 = da1 * sigmoid_deriv(a1)
    dw1 = (X.T @ dz1) / 4
    db1 = np.sum(dz1, axis=0) / 4
    
    # Update
    w2 -= current_lr * dw2
    b2 -= current_lr * db2
    w1 -= current_lr * dw1
    b1 -= current_lr * db1
    
    if epoch % 50 == 0:
        pred = (a2 > 0.5).astype(int).flatten()
        acc = (pred == y.flatten()).mean() * 100
        print(f"Эпоха {epoch:3d} | Loss: {loss:.6f} | Время: {global_time:.1f} | Скорость: {speed:.2f}x | Acc: {acc:.0f}%")

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ XOR:")
print("="*60)
pred = (a2 > 0.5).astype(int).flatten()
for i in range(4):
    print(f"  {'✅' if pred[i]==y[i][0] else '❌'} {X[i][0]} ⊕ {X[i][1]} = {pred[i]}")
print(f"\nТочность: {(pred == y.flatten()).mean() * 100:.0f}%")
print(f"Всего времени: {global_time:.1f}")
print("="*60)
input("\nНажми Enter...")
