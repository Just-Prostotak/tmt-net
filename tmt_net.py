"""
TMT-Net v25.0 - ПРИТЯЖЕНИЕ БУДУЩЕГО
Новый закон: цель имеет гравитацию
"""

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

X = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([[0], [1], [1], [0]])

np.random.seed(42)
w1 = np.random.randn(2, 8) * 0.5
b1 = np.zeros(8)
w2 = np.random.randn(8, 1) * 0.5
b2 = np.zeros(1)

time = 0.0
horizon = 1000
memory_w1, memory_w2 = [], []

print("="*70)
print("TMT-Net v25.0 - ПРИТЯЖЕНИЕ БУДУЩЕГО")
print("Новый закон: правильный ответ притягивает как гравитация")
print("="*70)

for epoch in range(400):
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # t = A
    mass1 = np.mean(np.abs(w1)) + 0.1
    mass2 = np.mean(np.abs(w2)) + 0.1
    action = (np.sum(np.abs(z1))*mass1 + np.sum(np.abs(z2))*mass2) / 8
    time += action
    
    # Инерция времени
    inertia = 1 + min(3.0, time / 50)
    
    # === НОВЫЙ ЗАКОН: ПРИТЯЖЕНИЕ БУДУЩЕГО ===
    # Расстояние до цели (ошибка)
    distance = np.mean(np.abs(a2 - y))
    # Гравитация цели: чем ближе, тем сильнее притяжение
    target_gravity = 1.0 / (distance + 0.1)
    # Полная скорость = инерция + притяжение
    speed = inertia + target_gravity
    speed = min(4.0, speed)  # горизонт скорости
    
    # Гомеостаз
    probs = a2.flatten()
    confidence = max(probs[0], 1-probs[0])
    fatigue = min(1.0, time / horizon)
    homeostasis = confidence * (1 - fatigue)
    
    # Горизонт
    if time >= horizon:
        print(f"  🕳️ КОЛЛАПС на эпохе {epoch} | Время: {time:.0f}")
        memory_w1.append(w1.copy())
        memory_w2.append(w2.copy())
        time = 0
        w1 += np.random.randn(*w1.shape) * 0.05
        w2 += np.random.randn(*w2.shape) * 0.05
    
    # Градиенты
    dz2 = a2 - y
    dw2 = (a1.T @ dz2) / 4
    db2 = np.sum(dz2, axis=0) / 4
    da1 = dz2 @ w2.T
    dz1 = da1 * (a1 * (1-a1))
    dw1 = (X.T @ dz1) / 4
    db1 = np.sum(dz1, axis=0) / 4
    
    # Обновление
    w2 -= speed * dw2
    b2 -= speed * db2
    w1 -= speed * dw1
    b1 -= speed * db1
    
    loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
    
    if epoch % 50 == 0:
        pred = (a2 > 0.5).astype(int).flatten()
        acc = (pred == y.flatten()).mean()*100
        print(f"Эпоха {epoch:3d} | Loss: {loss:.6f} | Acc: {acc:.0f}% | "
              f"Время: {time:.0f} | Скор: {speed:.2f}x | "
              f"Тяготение: {target_gravity:.2f} | Гомеостаз: {homeostasis:.3f}")

print("\n" + "="*70)
print("РЕЗУЛЬТАТЫ XOR:")
print("="*70)
pred = (a2 > 0.5).astype(int).flatten()
for i in range(4):
    print(f"  {'✅' if pred[i]==y[i][0] else '❌'} {X[i][0]} ⊕ {X[i][1]} = {pred[i]}")
print(f"\nТочность: {(pred==y.flatten()).mean()*100:.0f}%")

print("\nЗАКОНЫ TMT v25.0:")
print("  0: t = A")
print("  1: Инерция времени")
print("  2: Масса как сопротивление")
print("  3: Горизонт событий")
print("  4: Коллапс и излучение")
print("  5: Гомеостаз")
print("  6: Принцип Ферма")
print("  7: SSD = Чёрная дыра")
print("  8: ПРИТЯЖЕНИЕ БУДУЩЕГО (target gravity)")
print("="*70)
input("\nНажми Enter...")
