"""
TMT-Net: Теория Метрики Транзакций
Время = Действие (t = A)
ПРОСТАЯ РАБОЧАЯ ВЕРСИЯ
"""

import numpy as np
import random
from collections import deque
import hashlib

class TNeuron:
    def __init__(self, nid, mass=1.0, horizon=100):
        self.id = nid
        self.mass = mass
        self.time = 0.0
        self.horizon = horizon
        self.memory = deque(maxlen=horizon)
        self.state = 0.0
        
    def step(self, signal):
        cost = self.mass * abs(signal)
        self.time += cost
        self.state = np.tanh(signal / (1 + self.mass))
        
        if self.time >= self.horizon:
            h = hashlib.sha256(str(self.state).encode()).hexdigest()[:8]
            self.memory.append(h)
            self.time = 0.0
            self.state += random.uniform(-0.01, 0.01)
        return self.state

class TMTLayer:
    def __init__(self, n_neurons, n_inputs):
        self.neurons = [TNeuron(i) for i in range(n_neurons)]
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.5
        self.biases = np.zeros(n_neurons)
        
    def forward(self, x):
        signals = x @ self.weights + self.biases
        out = np.array([n.step(s) for n, s in zip(self.neurons, signals)])
        return out

class TMTModel:
    def __init__(self, sizes=[2, 4, 2]):
        self.layers = []
        for i in range(len(sizes)-1):
            self.layers.append(TMTLayer(sizes[i+1], sizes[i]))
        self.global_time = 0
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        # Softmax
        exp_x = np.exp(x - np.max(x))
        return exp_x / (np.sum(exp_x) + 1e-8)
    
    def predict(self, x):
        return np.argmax(self.forward(x))
    
    def train_step(self, x, y, lr=0.1):
        # Прямой проход с сохранением
        activations = [x]
        current = x
        for layer in self.layers:
            current = layer.forward(current)
            activations.append(current)
        
        # Выход и ошибка
        probs = activations[-1]
        error = -np.log(probs[y] + 1e-8)
        
        # Градиент для выходного слоя
        grad = probs.copy()
        grad[y] -= 1
        
        # Обратное распространение
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            inp = activations[i]
            
            # Обновление весов
            for j in range(layer.weights.shape[0]):
                for k in range(layer.weights.shape[1]):
                    layer.weights[j, k] -= lr * inp[j] * grad[k]
            
            # Обновление смещений
            for k in range(len(layer.biases)):
                layer.biases[k] -= lr * grad[k]
            
            # Обновление масс (t = A)
            for k, n in enumerate(layer.neurons):
                n.mass += abs(grad[k]) * lr * 0.05
                n.mass = max(0.1, min(3.0, n.mass))
            
            # Проброс градиента
            if i > 0:
                new_grad = np.zeros(len(inp))
                for j in range(len(inp)):
                    for k in range(len(grad)):
                        new_grad[j] += grad[k] * layer.weights[j, k]
                grad = new_grad * (1 - activations[i]**2)
        
        # Обновление глобального времени
        self.global_time = sum(n.time for l in self.layers for n in l.neurons)
        return error


# ============================================
# ТЕСТ
# ============================================
print("="*60)
print("TMT-Net: Теория Метрики Транзакций")
print("Формула: Время = Действие (t = A)")
print("="*60)

# Модель для XOR
model = TMTModel(sizes=[2, 8, 2])  # 2 входа, 8 нейронов, 2 выхода
X = np.array([[0,0], [0,1], [1,0], [1,1]], dtype=float)
Y = np.array([0, 1, 1, 0])

print("\nОбучение XOR...")
print("-"*40)

for epoch in range(500):
    total_error = 0
    # Перемешиваем данные
    indices = [0,1,2,3]
    random.shuffle(indices)
    
    for idx in indices:
        err = model.train_step(X[idx], Y[idx], lr=0.3)
        total_error += err
    
    if epoch % 100 == 0:
        correct = sum(1 for i in range(4) if model.predict(X[i]) == Y[i])
        print(f"Эпоха {epoch:4d} | Ошибка: {total_error/4:.4f} | Точность: {correct}/4 | Время: {model.global_time:.1f}")

print("\n" + "="*60)
print("РЕЗУЛЬТАТЫ XOR")
print("="*60)

correct = 0
for i in range(4):
    x = X[i]
    y = Y[i]
    p = model.predict(x)
    if p == y:
        correct += 1
        print(f"  ✅ {int(x[0])} XOR {int(x[1])} = {p} (цель={y})")
    else:
        print(f"  ❌ {int(x[0])} XOR {int(x[1])} = {p} (цель={y})")

print(f"\n🎯 ТОЧНОСТЬ: {correct}/4 ({correct*25}%)")

# Статистика
total_collapses = sum(len(n.memory) for l in model.layers for n in l.neurons)
total_mass = sum(n.mass for l in model.layers for n in l.neurons)

print(f"\n📊 СТАТИСТИКА TMT:")
print(f"  Коллапсов: {total_collapses}")
print(f"  Общая масса: {total_mass:.2f}")
print(f"  Глобальное время: {model.global_time:.2f}")

print("\n" + "="*60)
print("ГОТОВО. t = A - работает!")
print("="*60)

# Ждем нажатия Enter
input("\nНажми Enter для выхода...")
