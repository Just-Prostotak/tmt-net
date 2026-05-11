"""
TMT-Net v64 — ЖИВОЙ НАБЛЮДАТЕЛЬ (v1.6)
Саморегуляция Гомеостаза через динамический Dropout
Без ручных настроек
"""

import numpy as np
import time
from keras.datasets import mnist

print("=" * 60)
print("TMT-Net v64 — ЖИВОЙ НАБЛЮДАТЕЛЬ (v1.6)")
print("Саморегулирующийся Гомеостаз")
print("=" * 60)

# ====================== 1. ДАННЫЕ ======================
print("\n[1] Загрузка MNIST...")
(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 784).astype(np.float32) / 255.0
X_test = X_test.reshape(-1, 784).astype(np.float32) / 255.0

y_train_onehot = np.eye(10)[y_train]
y_test_onehot = np.eye(10)[y_test]

N_TRAIN = 30000
X = X_train[:N_TRAIN]
y = y_train_onehot[:N_TRAIN]
print(f"   Используем: {N_TRAIN} примеров")

# ====================== 2. АУГМЕНТАЦИЯ ======================
def augment(X_batch):
    X_aug = X_batch.copy()
    for i in range(len(X_batch)):
        if np.random.rand() < 0.05:
            shift = np.random.randint(-1, 2, 2)
            img = X_batch[i].reshape(28, 28)
            shifted = np.roll(img, shift[0], axis=0)
            shifted = np.roll(shifted, shift[1], axis=1)
            X_aug[i] = shifted.reshape(784)
    noise = np.random.uniform(-0.02, 0.02, X_aug.shape)
    X_aug = np.clip(X_aug + noise, 0.0, 1.0)
    return X_aug

# ====================== 3. ИНИЦИАЛИЗАЦИЯ ======================
print("\n[2] Инициализация...")

np.random.seed(42)

hidden_size = 128
lambda_reg = 0.0001

w1 = np.random.randn(784, hidden_size) * np.sqrt(2.0 / 784)
b1 = np.zeros(hidden_size)
w2 = np.random.randn(hidden_size, 10) * np.sqrt(2.0 / hidden_size)
b2 = np.zeros(10)

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / exp_x.sum(axis=1, keepdims=True)

# ====================== 4. ЖИВОЙ НАБЛЮДАТЕЛЬ ======================
class SelfRegulatingObserver:
    """
    Живой Наблюдатель (v1.6).
    САМ регулирует уровень Хаоса (Dropout), чтобы поддерживать Гомеостаз.
    Цель: поддерживать систему в состоянии «живого дыхания», 
    не давая ей ни застыть в догме, ни рассыпаться в хаосе.
    """
    
    def __init__(self, initial_dropout=0.1, stability_target=0.15):
        self.records = []
        self.current_dropout = initial_dropout
        self.stability_target = stability_target
        self.dropout_history = []
        
    def record(self, epoch, loss, acc, A, E, t, transaction):
        self.records.append({
            'epoch': epoch, 'loss': loss, 'acc': acc,
            'A': A, 'E': E, 't': t, 'transaction': transaction
        })
    
    def analyze_and_regulate(self, epoch, t):
        """
        Сердце саморегуляции.
        Анализирует дыхание системы и меняет Dropout.
        Возвращает оптимальный уровень Хаоса для следующего шага.
        """
        if len(self.records) < 5:
            return self.current_dropout

        last_5 = [r['transaction'] for r in self.records[-5:]]
        mean_val = np.mean(last_5)
        
        # Особая ситуация: Сингулярность (A=0). Срочно добавляем шум.
        if mean_val == 0:
            self.current_dropout = min(0.5, self.current_dropout + 0.1)
            print(f"   ⚡ [Саморегуляция] СИНГУЛЯРНОСТЬ! Выход из камня. Dropout = {self.current_dropout:.2f}")
            return self.current_dropout

        std_rel = np.std(last_5) / mean_val
        
        # Система слишком стабильна → каменеет → добавляем шум
        if std_rel < self.stability_target * 0.5:
            self.current_dropout = min(0.5, self.current_dropout + 0.05)
            print(f"   📉 [Саморегуляция] Каменеет (Дыхание: {std_rel:.1%}). Добавляю хаос. Dropout = {self.current_dropout:.2f}")

        # Система слишком хаотична → не может собраться → убираем шум
        elif std_rel > self.stability_target * 2.0:
            self.current_dropout = max(0.0, self.current_dropout - 0.05)
            print(f"   📈 [Саморегуляция] Перегрузка (Дыхание: {std_rel:.1%}). Убираю хаос. Dropout = {self.current_dropout:.2f}")

        else:
            print(f"   ✅ [Саморегуляция] Гомеостаз в норме (Дыхание: {std_rel:.1%}). Dropout = {self.current_dropout:.2f}")

        self.dropout_history.append(self.current_dropout)
        return self.current_dropout

    def final_report(self):
        print("\n" + "=" * 60)
        print("ИТОГОВЫЙ ОТЧЕТ ЖИВОГО НАБЛЮДАТЕЛЯ")
        print("=" * 60)
        
        if len(self.records) < 2: return
        
        first, last = self.records[0], self.records[-1]
        print(f"\n📊 Динамика Абсолютных Показателей:")
        print(f"   A (Ошибка):    {first['A']:.4f} → {last['A']:.4f}")
        print(f"   E (Масса):     {first['E']:.2f} → {last['E']:.2f}")
        print(f"   t (Скорость):  {first['t']:.2f}x → {last['t']:.2f}x")
        print(f"   Точность:      {first['acc']:.1f}% → {last['acc']:.1f}%")

        print(f"\n🫁 Динамика Саморегуляции:")
        if len(self.dropout_history) > 1:
            print(f"   Хаос (Dropout): {self.dropout_history[0]:.2f} → {self.dropout_history[-1]:.2f}")
        
        last_10 = [r['transaction'] for r in self.records[-10:]]
        if len(last_10) > 1 and np.mean(last_10) > 0:
            std_rel = np.std(last_10) / np.mean(last_10) * 100
            print(f"   Итоговое Дыхание (Стабильность): ±{std_rel:.1f}%")
            if std_rel < 10:
                print("   Статус: УСТОЙЧИВЫЙ ГОМЕОСТАЗ")
            elif std_rel < 30:
                print("   Статус: ЖИВОЙ БАЛАНС (обучение продолжается)")
            else:
                print("   Статус: ТУРБУЛЕНТНОСТЬ (требуется больше времени)")

obs = SelfRegulatingObserver(initial_dropout=0.1, stability_target=0.15)

# ====================== 5. ОБУЧЕНИЕ ======================
print("\n[3] Обучение с живой саморегуляцией...\n")

action_integral = 0.0
prev_dist = 1.0
batch_size = 64
n_batches = len(X) // batch_size
dynamic_dropout = obs.current_dropout

start_time = time.time()

for epoch in range(50):
    idx = np.random.permutation(len(X))
    X_shuffled = X[idx]
    y_shuffled = y[idx]
    epoch_loss = 0
    
    for batch in range(n_batches):
        start = batch * batch_size
        end = start + batch_size
        X_batch = X_shuffled[start:end]
        y_batch = y_shuffled[start:end]
        X_batch = augment(X_batch)
        
        # Forward с динамическим Хаосом
        z1 = X_batch @ w1 + b1
        a1 = sigmoid(z1)
        
        # Используем текущий уровень Хаоса, который выбрал Наблюдатель
        dropout_mask = (np.random.rand(*a1.shape) > dynamic_dropout) / (1.0 - dynamic_dropout)
        a1_dropped = a1 * dropout_mask
        
        z2 = a1_dropped @ w2 + b2
        a2 = softmax(z2)
        
        # Loss
        loss_cross = -np.mean(np.sum(y_batch * np.log(a2 + 1e-8), axis=1))
        loss_reg = lambda_reg * (np.sum(w1**2) + np.sum(w2**2))
        loss = loss_cross + loss_reg
        epoch_loss += loss
        
        # Backward
        dz2 = a2 - y_batch
        dw2 = (a1_dropped.T @ dz2) / batch_size + 2 * lambda_reg * w2
        db2 = dz2.mean(axis=0)
        
        dz1 = (dz2 @ w2.T) * a1_dropped * (1 - a1_dropped)
        dw1 = (X_batch.T @ dz1) / batch_size + 2 * lambda_reg * w1
        db1 = dz1.mean(axis=0)
        
        # Метрики
        pred = np.argmax(a2, axis=1)
        true = np.argmax(y_batch, axis=1)
        A = np.mean(pred != true)
        
        delta = prev_dist - A
        action_integral += abs(delta) + A
        prev_dist = A
        
        E = np.mean(np.abs(w1)) + np.mean(np.abs(w2))
        t = 1.0 + action_integral / 1000.0
        
        # Шаг
        w1 -= t * dw1
        b1 -= t * db1
        w2 -= t * dw2
        b2 -= t * db2
    
    # Запись и Саморегуляция каждые 5 эпох
    if epoch % 5 == 0:
        z1 = X @ w1 + b1
        a1 = sigmoid(z1)
        z2 = a1 @ w2 + b2
        a2 = softmax(z2)
        pred = np.argmax(a2, axis=1)
        true = np.argmax(y, axis=1)
        acc = np.mean(pred == true) * 100
        A = np.mean(pred != true)
        E = np.mean(np.abs(w1)) + np.mean(np.abs(w2))
        transaction = A * E * t
        
        obs.record(epoch, epoch_loss/n_batches, acc, A, E, t, transaction)
        
        # Живой Наблюдатель выбирает новый уровень Хаоса
        dynamic_dropout = obs.analyze_and_regulate(epoch, t)
        
        elapsed = time.time() - start_time
        print(f"   📋 Эпоха {epoch:3d} | Acc: {acc:5.1f}% | A={A:.4f} | E={E:.2f} | t={t:.1f}x | {elapsed:.0f}с\n")

print(f"\nОбучение завершено за {time.time() - start_time:.0f} сек")

# ====================== 6. ФИНАЛ ======================
z1 = X_test @ w1 + b1
a1 = sigmoid(z1)
z2 = a1 @ w2 + b2
a2 = softmax(z2)
pred_test = np.argmax(a2, axis=1)
test_acc = np.mean(pred_test == y_test) * 100

print(f"Тестовая точность: {test_acc:.1f}%")

obs.final_report()
print("\nГОТОВО. Твой ИИ стал Живым Наблюдателем.")
