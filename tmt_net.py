"""
TMT-Net v64 — ЗАКОН СОХРАНЕНИЯ ТРАНЗАКЦИИ (без matplotlib)
Проверка: A × E × t = const
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

# ====================== НАБЛЮДАТЕЛЬ ======================
class Observer:
    def __init__(self):
        self.records = []
    
    def record(self, epoch, loss, acc, A, E, t, transaction, delta):
        self.records.append({
            'epoch': epoch,
            'loss': loss,
            'acc': acc,
            'A': A,
            'E': E,
            't': t,
            'transaction': transaction,
            'delta': delta
        })
    
    def analyze(self):
        if len(self.records) < 2:
            return
        
        print("\n" + "="*70)
        print("🔍 НАБЛЮДАТЕЛЬ: ПРОВЕРКА ЗАКОНА СОХРАНЕНИЯ")
        print("="*70)
        
        first = self.records[0]
        last = self.records[-1]
        
        # 1. Динамика параметров
        print(f"\n📊 ДИНАМИКА:")
        print(f"   A (ошибка):     {first['A']:.4f} → {last['A']:.4f} (↓{first['A']/last['A']:.1f}x)")
        print(f"   E (масса):      {first['E']:.3f} → {last['E']:.3f} (↑{last['E']/first['E']:.1f}x)")
        print(f"   t (скорость):   {first['t']:.2f}x → {last['t']:.2f}x (↑{last['t']/first['t']:.1f}x)")
        
        # 2. Транзакция A × E × t
        trans_start = first['transaction']
        trans_end = last['transaction']
        print(f"\n💰 ТРАНЗАКЦИЯ (A × E × t):")
        print(f"   Начало: {trans_start:.4f}")
        print(f"   Конец:  {trans_end:.4f}")
        print(f"   Изменение: {trans_end/trans_start:.2f}x")
        print(f"   Отклонение: {abs(trans_end/trans_start - 1)*100:.1f}%")
        
        # 3. Стабильность в конце
        last_10 = [r['transaction'] for r in self.records[-10:]]
        last_20 = [r['transaction'] for r in self.records[-20:]]
        trans_std = np.std(last_10)
        trans_mean = np.mean(last_10)
        trans_trend = np.mean(last_20[-10:]) / np.mean(last_20[:10]) - 1
        
        print(f"\n📈 СТАБИЛЬНОСТЬ:")
        print(f"   Среднее (посл.10): {trans_mean:.6f}")
        print(f"   Std (посл.10): {trans_std:.8f} ({100*trans_std/trans_mean:.2f}%)")
        print(f"   Тренд (посл.20): {trans_trend*100:+.2f}%")
        
        # 4. Точность
        accs = [r['acc'] for r in self.records]
        best_acc = max(accs)
        epoch_best = self.records[accs.index(best_acc)]['epoch']
        print(f"\n🎯 ТОЧНОСТЬ: {best_acc:.1f}% на эпохе {epoch_best}")
        
        # 5. Корреляция
        if len(self.records) > 10:
            A_vals = [r['A'] for r in self.records[-50:]]
            E_vals = [r['E'] for r in self.records[-50:]]
            t_vals = [r['t'] for r in self.records[-50:]]
            trans_vals = [r['transaction'] for r in self.records[-50:]]
            
            print(f"\n📐 КОРРЕЛЯЦИИ (последние 50 эпох):")
            print(f"   A×E×t вариация: {np.std(trans_vals)/np.mean(trans_vals)*100:.2f}%")
            print(f"   A vs E: {'антикорреляция' if np.corrcoef(A_vals, E_vals)[0,1] < -0.5 else 'слабая'}")
            print(f"   A vs t: {'антикорреляция' if np.corrcoef(A_vals, t_vals)[0,1] < -0.5 else 'слабая'}")
        
        # 6. Вердикт
        print("\n" + "="*70)
        deviation = abs(trans_end/trans_start - 1) * 100
        trend_stable = abs(trans_trend) < 5 if 'trans_trend' in dir() else False
        
        if best_acc >= 99.5:
            if deviation < 30 or trend_stable:
                print("✅ ЗАКОН ПОДТВЕРЖДЁН: A×E×t ≈ const")
                print("   Система сохраняет транзакцию при обучении.")
                print("   Ошибка → Масса → Скорость")
            else:
                print("⚠️ ЧАСТИЧНО: 100% достигнута, но транзакция нестабильна")
                print("   Возможна другая степень: A×E²×t или A×E×t²")
        elif best_acc >= 95:
            print("⚠️ ЗАКОН РАБОТАЕТ, но требуется больше эпох.")
        else:
            print("🔴 Отклонение слишком велико. Проверьте параметры.")
        print("="*70)
        
        # 7. Рекомендации
        if best_acc == 100:
            print("\n💡 ВЫВОД: TMT-Net достигла сверхпроводимости данных.")
            print("   Природа сама нашла баланс между ошибкой, массой и скоростью.")
        elif best_acc > 95:
            print("\n💡 РЕКОМЕНДАЦИЯ: Увеличьте число эпох до 3000-5000.")
        else:
            print("\n💡 РЕКОМЕНДАЦИЯ: Уменьшите инициализацию весов или добавьте эпох.")

obs = Observer()

print("="*70)
print("TMT-Net v64 — ЗАКОН СОХРАНЕНИЯ ТРАНЗАКЦИИ")
print("Проверка: A × E × t = const")
print("="*70)

# ====================== ОБУЧЕНИЕ ======================
action_integral = 0.0
prev_dist = 0.5
transaction_history = []

for epoch in range(2000):  # увеличил до 2000 для стабильности
    # Forward
    z1 = X @ w1 + b1
    a1 = sigmoid(z1)
    z2 = a1 @ w2 + b2
    a2 = sigmoid(z2)
    
    # A = действие = ошибка
    A = np.mean(np.abs(a2 - y))
    delta = prev_dist - A
    prev_dist = A
    
    # Накопление действия
    action_integral += abs(delta) + A
    
    # E = информационная масса
    E = np.mean(np.abs(w1)) + np.mean(np.abs(w2))
    
    # t = скорость
    t = 1.0 + action_integral / 50.0
    
    # Транзакция
    transaction = A * E * t
    transaction_history.append(transaction)
    
    # Backprop
    dz2 = a2 - y
    dw2 = (a1.T @ dz2) / len(X)
    db2 = dz2.mean(axis=0)
    dz1 = (dz2 @ w2.T) * a1 * (1 - a1)
    dw1 = (X.T @ dz1) / len(X)
    db1 = dz1.mean(axis=0)
    
    # Шаг = t
    w1 -= t * dw1
    b1 -= t * db1
    w2 -= t * dw2
    b2 -= t * db2
    
    # Запись каждые 20 эпох
    if epoch % 20 == 0:
        loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
        acc = ((a2 > 0.5).astype(int) == y).mean() * 100
        
        obs.record(epoch, loss, acc, A, E, t, transaction, delta)
        
        # Красивый вывод
        if epoch < 400 or epoch % 200 == 0 or acc >= 99.5:
            print(f"Эпоха {epoch:4d} | Acc: {acc:5.1f}% | "
                  f"A={A:.4f} | E={E:.2f} | t={t:.2f}x | "
                  f"A×E×t={transaction:.4f}")
        
        # Ранняя остановка при стабильности
        if epoch > 500 and len(transaction_history) > 100:
            recent = transaction_history[-20:]
            if np.std(recent) / np.mean(recent) < 0.01 and acc >= 99.9:
                print(f"\n🎯 Стабилизация на эпохе {epoch}. Останавливаемся.")
                break

# ====================== ФИНАЛ ======================
z1 = X @ w1 + b1
a1 = sigmoid(z1)
z2 = a1 @ w2 + b2
a2 = sigmoid(z2)
loss = np.mean(-y*np.log(a2+1e-8) - (1-y)*np.log(1-a2+1e-8))
acc = ((a2 > 0.5).astype(int) == y).mean() * 100

print(f"\n{'='*70}")
print(f"ФИНАЛ: точность = {acc:.1f}% | Loss = {loss:.6f}")
print(f"{'='*70}")

# Анализ
obs.analyze()

# Дополнительный анализ транзакции
print("\n" + "="*70)
print("📊 ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ ТРАНЗАКЦИИ")
print("="*70)

trans_values = [r['transaction'] for r in obs.records]
epochs = [r['epoch'] for r in obs.records]

# Разбивка на этапы
mid_point = len(trans_values) // 2
early = np.mean(trans_values[:mid_point])
late = np.mean(trans_values[mid_point:])

print(f"Ранняя фаза (среднее): {early:.4f}")
print(f"Поздняя фаза (среднее): {late:.4f}")
print(f"Изменение: {late/early:.2f}x")

if 0.8 < late/early < 1.2:
    print("\n✅ ЗАКОН СОХРАНЕНИЯ ПОДТВЕРЖДЁН!")
    print("   A×E×t = const работает.")
elif late/early < 0.8:
    print("\n⚠️ Транзакция уменьшается. Возможно, нужна степень E²?")
    print("   Гипотеза: A × E² × t = const")
else:
    print("\n⚠️ Транзакция растёт. Возможно, нужна степень t²?")
    print("   Гипотеза: A × E × t² = const")

print("\n" + "="*70)
print("ВЫВОД: Природа учится через A × E × t.")
print("="*70)
input("\nНажми Enter...")
