"""
TMT-Net: Теория Метрики Транзакций
Время = Действие (t = A)
Минимальная рабочая основа
"""

import numpy as np
import random
from collections import deque
import hashlib

# ============================================
# НЕЙРОН
# ============================================
class TNeuron:
    def __init__(self, nid, mass=1.0, horizon=100):
        self.id = nid
        self.mass = mass
        self.time = 0.0
        self.horizon = horizon
        self.memory = deque(maxlen=horizon)
        self.state = 0.0
        self.collapse_count = 0
        
    def step(self, signal):
        cost = self.mass * abs(signal)
        self.time += cost
        self.state = np.tanh(signal / (1 + self.mass))
        
        if self.time >= self.horizon:
            h = hashlib.sha256(str(self.state).encode()).hexdigest()[:8]
            self.memory.append(h)
            self.time = 0.0
            self.state += random.uniform(-0.01, 0.01)
            self.collapse_count += 1
        return self.state


# ============================================
# СЛОЙ
# ============================================
class TMTLayer:
    def __init__(self, n_neurons, n_inputs):
        self.neurons = [TNeuron(i) for i in range(n_neurons)]
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.1
        self.biases = np.zeros(n_neurons)
        
    def forward(self, x):
        signals = x @ self.weights + self.biases
        out = np.array([n.step(s) for n, s in zip(self.neurons, signals)])
        return out


# ============================================
# МОДЕЛЬ
# ============================================
class TMTModel:
    def __init__(self, sizes=[2, 4, 2]):
        self.layers = [TMTLayer(sizes[i+1], sizes[i]) for i in range(len(sizes)-1)]
        self.global_time = 0
        self.loss_history = []
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        x = x - x.max()
        ex = np.exp(x)
        return ex / (ex.sum() + 1e-8)
    
    def predict(self, x):
        return np.argmax(self.forward(x))
    
    def train_step(self, x, y, lr=0.05):
        # Прямой проход с кэшем
        layer_inputs = [x]
        current = x
        for layer in self.layers:
            layer_inputs.append(current)
            current = layer.forward(current)
        
        probs = current
        target = np.zeros(probs.shape)
        target[y] = 1
        
        # Гравитационное обновление
        delta = target - probs
        
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            inp = layer_inputs[i]
            
            # Обновление весов (гравитация ошибки)
            grad_weights = np.outer(inp, delta)
            grad_biases = delta.copy()
            layer.weights += lr * grad_weights
            layer.biases += lr * grad_biases
            
            # Обновление масс нейронов
            for k, n in enumerate(layer.neurons):
                if k < len(delta) and abs(delta[k]) > 0.01:
                    n.mass += abs(delta[k]) * lr * 0.1
                else:
                    n.mass = max(0.1, n.mass - lr * 0.001)
            
            # Проброс ошибки назад
            if i > 0:
                delta = (delta @ layer.weights.T) * (1 - layer_inputs[i]**2)
                delta = np.clip(delta, -1, 1)
        
        error = np.abs(probs - target).sum()
        self.global_time = sum(n.time for l in self.layers for n in l.neurons)
        self.loss_history.append(error)
        return error


# ============================================
# БЫСТРЫЙ ТЕСТ
# ============================================
if __name__ == "__main__":
    print("="*50)
    print("TMT-Net v1.0")
    print("Время = Действие (t = A)")
    print("="*50)
    
    # XOR задача
    model = TMTModel(sizes=[2, 6, 2])
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    Y = np.array([0, 1, 1, 0])
    
    for epoch in range(200):
        loss = 0
        for x, y in zip(X, Y):
            loss += model.train_step(x, y, lr=0.1)
        
        if epoch % 50 == 0:
            acc = sum(1 for x, y in zip(X, Y) if model.predict(x) == y)
            print(f"Эпоха {epoch:3d} | Ошибка: {loss/4:.4f} | Точность: {acc}/4")
    
    print("\nРезультаты XOR:")
    for x, y in zip(X, Y):
        p = model.predict(x)
        print(f"  {x[0]} ⊕ {x[1]} = {p} (цель={y}) {'✓' if p==y else '✗'}")
    
    print("\nГотово. t = A.")
