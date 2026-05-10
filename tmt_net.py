"""
TMT-Net v63 — НАБЛЮДАТЕЛЬ
Только t = A = E * t. Никаких добавок.
Смотрим, что природа делает сама.
"""

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

# ====================== ДАННЫЕ ======================
np.random.seed(42)
n = 100
r0 = np.random.rand(n) * 3.0
a0 = np.random.rand(n) * 2 * np.pi
X0 = np.column_stack([r0 * np.cos(a0), r0 * np.sin(a0)])
r1 = 3.0 + np.random.rand(n) * 3.0
a1 = np.random.rand(n) * 2 * np.pi
X1 = np.column_stack([r1 * np.cos(a1), r1 * np.sin(a1)])
X = np.vstack([X0, X1]) / 6.0
y = np.vstack([np.zeros((n,1)), np.ones((n,1))])

# ====================== ИНИЦИАЛИЗАЦИЯ ======================
np.random.seed(42)
w1 = np.random.randn(2, 16) * 0.5
b1 = np.zeros(16)
w2 = np.random.randn(16, 1) * 0.5
b2 = np.zeros(1)

time = 0.0

# ====================== НАБЛЮДАТЕЛЬ ======================
class Observer:
    def __init__(self):
        self.records = []
    
    def record(self, epoch, loss, acc, dist, time, speed, mass_w1, mass_w2, delta):
        self.records.append({
            'epoch': epoch,
            'loss': loss,
            'acc': acc,
            'dist': dist,
            'time': time,
            'speed': speed,
            'mass_w1': mass_w1,
            'mass_w2': mass_w2,
            'delta': delta
        })
    
    def analyze(self):
        if len(self.records) < 2:
            return
        
        print("\n" + "="*70)
        print("🔍 НАБЛЮДАТЕЛЬ: ЧТО ОБНАРУЖЕНО")
        print("="*70)
        
        # 1. Рост массы
        first_mass = self.records[0]['mass_w1'] + self.records[0]['mass_w2']
        last_mass = self.records[-1]['mass_w1'] + self.records[-1]['mass_w2']
        print(f"1. Масса весов: {first_mass:.3f} → {last_mass:.3f} (рост в {last_mass/first_mass:.1f} раз)")
        
        # 2. Стабилизация скорости
        speeds = [r['speed'] for r in self.records]
        max_speed = max(speeds)
        epoch_max_speed = self.records[speeds.index(max_speed)]['epoch']
        print(f"2. Пик скорости: {max_speed:.2f}x на эпохе {epoch_max_speed}")
        
        # 3. Лучшая точность
        accs = [r['acc'] for r in self.records]
        best_acc = max(accs)
        epoch_best = self.records[accs.index(best_acc)]['epoch']
        print(f"3. Лучшая точность: {best_acc:.1f}% на эпохе {epoch_best}")
        
        # 4. Когда сеть замедлилась
        slow_epochs = [r['epoch'] for r in self.records if r['speed'] < 1.1 and r['epoch'] > 50]
        if slow_epochs:
            print(f"4. Замедление: первые признаки на эпохе {slow_epochs[0]}")
        
        # 5. Связь массы и точности
        masses = [r['mass_w1'] + r['mass_w2'] for r in self.records]
        if len(masses) > 10:
            early_mass = np.mean(masses[:len(masses)//3])
            late_mass = np.mean(masses[-len(masses)//3:])
            print(f"5. Масса (начало): {early_mass:.3f} → (конец): {late_mass:.3f}")
        
        # 6. Дельта (изменение расстояния)
        deltas = [r['delta'] for r in self.records]
        positive_deltas = sum(1 for d in deltas if d > 0)
        print(f"6. Улучшения: {positive_deltas}/{len(deltas)} шагов ({100*positive_deltas/len(deltas):.0f}%)")
        
        # 7. Самоорганизация
        if best_acc >= 95 and epoch_best < len(self.records) * 0.7:
            print(f"7. 🎯 Сеть нашла решение сама, задолго до конца обучения!")
        
        # 8. U-образная кривая?
        mid_acc = np.mean(accs[len(accs)//3:2*len(accs)//3])
        if best_acc > mid_acc * 1.1 and mid_acc < 80:
            print(f"8. 📈 Обнаружена U-образная кривая: провал в середине, рост в конце")

obs = Observer()

print("="*70)
print("TMT-Net v63 — ТОЛЬКО ЯДРО + НАБЛЮДАТЕЛЬ")
print("Законов: 1 (t = A). Всё остальное — сама природа.")
print("="*70)

prev_dist = 0.5

for epoch in range(1500):
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    dist = np.mean(np.abs(a2 - y))
    delta = prev_dist - dist
    
    # === ТОЛЬКО ЯДРО ===
    time += abs(delta) + dist
    speed = 1.0 + time / 50.0
    # ====================
    
    prev_dist = dist
    
    # Backprop
    dz2 = a2 - y
    dw2 = (a1.T @ dz2) / len(X)
    db2 = dz2.mean(axis=0)
    dz1 = (dz2 @ w2.T) * a1 * (1 - a1)
    dw1 = (X.T @ dz1) / len(X)
    db1 = dz1.mean(axis=0)
    
    w1 -= speed * dw1
    b1 -= speed * db1
    w2 -= speed * dw2
    b2 -= speed * db2
    
    # Запись каждые 10 эпох
    if epoch % 10 == 0:
        loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
        acc = ((a2 > 0.5).astype(int) == y).mean() * 100
        mass1 = np.mean(np.abs(w1))
        mass2 = np.mean(np.abs(w2))
        obs.record(epoch, loss, acc, dist, time, speed, mass1, mass2, delta)
    
    if epoch % 200 == 0:
        loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
        acc = ((a2 > 0.5).astype(int) == y).mean() * 100
        print(f"Эпоха {epoch:4d} | Loss: {loss:.4f} | Acc: {acc:.1f}% | Dist: {dist:.4f} | Time: {time:.0f} | Speed: {speed:.2f}x")

# Финальный результат
loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
acc = ((a2 > 0.5).astype(int) == y).mean() * 100
print(f"\nФинальная точность: {acc:.1f}%")

# Анализ
obs.analyze()

print("\n" + "="*70)
print("ВЫВОД: Ядро работает. Природа сама всё остальное.")
print("="*70)
input("\nНажми Enter...")
