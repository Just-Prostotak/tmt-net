"""
TMT-Net v24.0 - ЧИСТАЯ ФИЗИКА
Без dt, без friction, без v_w
Только: время, масса, действие
"""

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Данные XOR
X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

# Инициализация
np.random.seed(42)
n_neurons = 8
w1 = np.random.randn(2, n_neurons) * 0.5
b1 = np.zeros(n_neurons)
w2 = np.random.randn(n_neurons, 1) * 0.5
b2 = np.zeros(1)

# TMT — ТОЛЬКО ВРЕМЯ И ДЕЙСТВИЕ
global_time = 0.0
horizon = 1000.0
memory = []  # черная дыра (память)

print("="*70)
print("TMT-Net v24.0 - ЧИСТАЯ ФИЗИКА")
print("Без dt, friction, v_w. Только t = A")
print("="*70)

for epoch in range(300):
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # ЗАКОН 0: t = A (Время = Действие)
    mass1 = np.mean(np.abs(w1)) + 0.1
    mass2 = np.mean(np.abs(w2)) + 0.1
    action = (np.sum(np.abs(z1)) * mass1 + np.sum(np.abs(z2)) * mass2) / 8
    global_time += action
    
    # ЗАКОН 1: Инерция времени (опыт ускоряет)
    speed = 1 + min(3.0, global_time / 50)
    
    # ЗАКОН 3: Горизонт событий (коллапс)
    if global_time >= horizon:
        print(f"  🕳️ КОЛЛАПС на эпохе {epoch}")
        memory.append(w1.copy())  # Закон 7: черная дыра
        w1 += np.random.randn(*w1.shape) * 0.05  # Закон 4: излучение
        w2 += np.random.randn(*w2.shape) * 0.05
        global_time = 0
    
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
    
    # ЗАКОН 6: Принцип Ферма (минимальный путь)
    # Обновление без dt, без friction, без v_w — только градиент!
    w2 -= speed * dw2
    b2 -= speed * db2
    w1 -= speed * dw1
    b1 -= speed * db1
    
    if epoch % 50 == 0:
        pred = (a2 > 0.5).astype(int).flatten()
        acc = (pred == y.flatten()).mean() * 100
        print(f"Эпоха {epoch:3d} | Loss: {loss:.6f} | Acc: {acc:.0f}% | "
              f"Время: {global_time:.0f} | Скорость: {speed:.2f}x")

print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ XOR:")
print("="*70)
z1 = X @ w1 + b1
a1 = sigmoid(z1)
z2 = a1 @ w2 + b2
a2 = sigmoid(z2)
pred = (a2 > 0.5).astype(int).flatten()
for i in range(4):
    print(f"  {'✅' if pred[i]==y[i][0] else '❌'} {X[i][0]} ⊕ {X[i][1]} = {pred[i]}")
print(f"\nТочность: {(pred == y.flatten()).mean() * 100:.0f}%")

print("\n" + "="*70)
print("ЧИСТАЯ ФИЗИКА TMT v24.0:")
print("="*70)
print("✅ dt = 1 (квант действия)")
print("✅ friction не нужен (энтропия в коллапсе)")
print("✅ v_w не нужен (импульс не обязателен)")
print("✅ Только: время, масса, градиент")
print(f"✅ Коллапсов: {len(memory)}")
print("="*70)
input("\nНажми Enter...")
