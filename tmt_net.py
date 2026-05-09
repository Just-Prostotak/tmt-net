"""
TMT-Net: Теория Метрики Транзакций
Время = Действие (t = A)
Минимальная нейросеть на принципах физики черных дыр.
Просто запусти: python tmt_net.py
"""

import numpy as np
import random
from collections import deque
import hashlib

# ============================================
# 1. НЕЙРОН
# ============================================
class TNeuron:
    def __init__(self, id, mass=1.0):
        self.id = id
        self.mass = mass            # масса = сопротивление
        self.time = 0.0             # локальное время
        self.horizon = 100          # горизонт событий
        self.memory = deque(maxlen=100)  # голографическая память
        self.state = 0.0            # текущее состояние
        
    def step(self, signal):
        cost = self.mass * abs(signal)   # стоимость = масса * сигнал
        self.time += cost                # время растет
        self.state = np.tanh(signal / (1 + self.mass))
        
        if self.time >= self.horizon:    # коллапс горизонта
            self._collapse()
        return self.state
    
    def _collapse(self):
        h = hashlib.sha256(str(self.state).encode()).hexdigest()[:8]
        self.memory.append(h)
        self.time = 0.0
        self.state += random.uniform(-0.01, 0.01)  # излучение Хокинга

# ============================================
# 2. СЛОЙ
# ============================================
class TMTLayer:
    def __init__(self, n_neurons, n_inputs):
        self.neurons = [TNeuron(i) for i in range(n_neurons)]
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.1
        
    def forward(self, x):
        signals = x @ self.weights
        out = np.array([n.step(s) for n, s in zip(self.neurons, signals)])
        return out

# ============================================
# 3. МОДЕЛЬ
# ============================================
class TMTModel:
    def __init__(self, sizes=[784, 128, 10]):
        self.layers = []
        for i in range(len(sizes)-1):
            self.layers.append(TMTLayer(sizes[i+1], sizes[i]))
        self.global_time = 0
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        x = x - x.max()
        ex = np.exp(x)
        return ex / ex.sum()
    
    def predict(self, x):
        return np.argmax(self.forward(x))
    
    def train_step(self, x, y, lr=0.01):
        probs = self.forward(x)
        target = np.zeros(probs.shape)
        target[y] = 1
        error = np.abs(probs - target).sum()
        
        for layer in self.layers:
            for n in layer.neurons:
                if n.time > n.horizon * 0.8:
                    n.mass += error * lr * 0.1
                else:
                    n.mass = max(0.1, n.mass - lr * 0.001)
        
        self.global_time = sum(n.time for l in self.layers for n in l.neurons)
        return error

# ============================================
# 4. ТЕСТ НА XOR
# ============================================
def test_xor():
    print("="*50)
    print("ТЕСТ: XOR задача")
    print("Формула: t = A (время = действие)")
    print("="*50)
    
    model = TMTModel(sizes=[2, 4, 2])
    
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    Y = np.array([0, 1, 1, 0])
    
    for epoch in range(200):
        loss = 0
        for x, y in zip(X, Y):
            loss += model.train_step(x, y, lr=0.05)
        
        if epoch % 40 == 0:
            print(f"Эпоха {epoch:3d} | Время: {model.global_time:8.2f} | Ошибка: {loss:.4f}")
    
    print("\nРезультаты:")
    for x, y in zip(X, Y):
        p = model.predict(x)
        print(f"  {x[0]} XOR {x[1]} = {p} (верно: {y}) {'✓' if p==y else '✗'}")
    
    print(f"\nФинальное глобальное время: {model.global_time:.2f}")

# ============================================
# 5. MNIST УПРОЩЕННЫЙ (DIGITS)
# ============================================
def test_digits():
    print("\n" + "="*50)
    print("ТЕСТ: Распознавание цифр (Digits 8x8)")
    print("="*50)
    
    try:
        from sklearn.datasets import load_digits
        from sklearn.model_selection import train_test_split
        
        digits = load_digits()
        X = digits.data / 16.0
        y = digits.target
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=400, random_state=42
        )
        
        model = TMTModel(sizes=[64, 32, 10])
        
        for epoch in range(50):
            loss = 0
            for x, y_true in zip(X_train, y_train):
                loss += model.train_step(x, y_true, lr=0.01)
            
            if epoch % 10 == 0:
                correct = sum(model.predict(x) == y for x, y in zip(X_test, y_test))
                acc = correct / len(y_test)
                print(f"Эпоха {epoch:3d} | Время: {model.global_time:8.2f} | "
                      f"Ошибка: {loss/len(X_train):.4f} | Точность: {acc:.2%}")
        
        correct = sum(model.predict(x) == y for x, y in zip(X_test, y_test))
        print(f"\nФинальная точность: {correct/len(y_test):.2%}")
        
    except ImportError:
        print("Нужен scikit-learn: pip install scikit-learn")

# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    test_xor()
    test_digits()
    
    print("\n" + "="*50)
    print("ГОТОВО. t = A.")
    print("="*50)
    
    # ВОТ ЭТО НЕ ДАСТ ОКНУ ЗАКРЫТЬСЯ:
    input("\nНажми Enter чтобы закрыть...")