"""
TMT-Net: Теория Метрики Транзакций
Время = Действие (t = A)
Нейросеть на принципах физики черных дыр.
"""

import numpy as np
import random
from collections import deque
import hashlib

# ============================================
# 1. БАЗОВЫЙ НЕЙРОН
# ============================================
class TNeuron:
    def __init__(self, id, mass=1.0, horizon=100):
        self.id = id
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
            self._collapse()
        return self.state
    
    def _collapse(self):
        h = hashlib.sha256(str(self.state).encode()).hexdigest()[:8]
        self.memory.append(h)
        self.time = 0.0
        self.state += random.uniform(-0.01, 0.01)


# ============================================
# 2. КВАНТОВЫЙ НЕЙРОН (наследуется от TNeuron)
# ============================================
class TNeuronQuantum(TNeuron):
    def __init__(self, id, mass=1.0, horizon=100):
        super().__init__(id, mass, horizon)
        self.entangled_partner = None  # связанный нейрон
        self.tunnel_prob = 0.1         # вероятность туннелирования
        
    def entangle(self, other):
        """Запутать с другим нейроном"""
        self.entangled_partner = other
        other.entangled_partner = self
        
    def step(self, signal):
        # Квантовое туннелирование: иногда пропускаем обработку
        if random.random() < self.tunnel_prob:
            return self.state  # возвращаем текущее состояние без затрат
        
        # Обычная обработка
        cost = self.mass * abs(signal)
        self.time += cost
        self.state = np.tanh(signal / (1 + self.mass))
        
        # Синхронизация с запутанным партнером (shared memory)
        if self.entangled_partner is not None:
            partner = self.entangled_partner
            self.state = (self.state + partner.state) / 2
            partner.state = self.state
        
        if self.time >= self.horizon:
            self._collapse()
        return self.state
    
    def _collapse(self):
        super()._collapse()
        # Квантовое излучение: отправляем сигнал запутанному партнеру
        if self.entangled_partner is not None:
            self.entangled_partner.state += random.uniform(-0.02, 0.02)


# ============================================
# 3. СЛОЙ
# ============================================
class TMTLayer:
    def __init__(self, n_neurons, n_inputs, neuron_type="classic"):
        if neuron_type == "quantum":
            self.neurons = [TNeuronQuantum(i) for i in range(n_neurons)]
        else:
            self.neurons = [TNeuron(i) for i in range(n_neurons)]
        self.weights = np.random.randn(n_inputs, n_neurons) * 0.1
        
    def forward(self, x):
        signals = x @ self.weights
        out = np.array([n.step(s) for n, s in zip(self.neurons, signals)])
        return out


# ============================================
# 4. МОДЕЛЬ
# ============================================
class TMTModel:
    def __init__(self, sizes=[2, 4, 2], neuron_types=None):
        """
        sizes: список размеров слоев [вход, скрытый1, ..., выход]
        neuron_types: список типов нейронов для каждого слоя (None = classic)
        """
        if neuron_types is None:
            neuron_types = ["classic"] * (len(sizes) - 1)
        
        self.layers = []
        for i in range(len(sizes) - 1):
            self.layers.append(
                TMTLayer(sizes[i+1], sizes[i], neuron_types[i])
            )
        self.global_time = 0
        
    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        x = x - x.max()
        ex = np.exp(x)
        return ex / (ex.sum() + 1e-10)
    
    def predict(self, x):
        return np.argmax(self.forward(x))
    
    def train_step(self, x, y, lr=0.01):
        # Прямой проход с сохранением входов слоев
        layer_inputs = [x]
        current = x
        for layer in self.layers:
            layer_inputs.append(current)
            current = layer.forward(current)
        
        probs = current
        target = np.zeros(probs.shape)
        target[y] = 1
        error = np.abs(probs - target).sum()
        delta = (probs - target) * lr
        
        # Обратный проход
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            inp = layer_inputs[i]
            
            # Обновляем ВЕСА
            layer.weights -= np.outer(inp, delta) * lr
            
            # Обновляем массы нейронов
            for j, n in enumerate(layer.neurons):
                if n.time > n.horizon * 0.8:
                    n.mass += abs(delta[j]) * lr * 0.1
                else:
                    n.mass = max(0.1, n.mass - lr * 0.001)
            
            # Пробрасываем delta на предыдущий слой
            if i > 0:
                delta = (delta @ layer.weights.T) * (1 - layer_inputs[i]**2)
                delta = np.clip(delta, -1, 1)
        
        self.global_time = sum(n.time for l in self.layers for n in l.neurons)
        return error


# ============================================
# 5. ТЕСТ XOR
# ============================================
def test_xor():
    print("="*50)
    print("ТЕСТ: XOR задача")
    print("Формула: t = A")
    print("="*50)
    
    model = TMTModel(sizes=[2, 4, 2])
    X = np.array([[0,0], [0,1], [1,0], [1,1]])
    Y = np.array([0, 1, 1, 0])
    
    for epoch in range(200):
        loss = sum(model.train_step(x, y, lr=0.05) for x, y in zip(X, Y))
        if epoch % 40 == 0:
            print(f"Эпоха {epoch:3d} | Время: {model.global_time:8.2f} | Ошибка: {loss:.4f}")
    
    print("\nРезультаты:")
    for x, y in zip(X, Y):
        p = model.predict(x)
        print(f"  {x[0]} XOR {x[1]} = {p} (={y}) {'OK' if p==y else 'FAIL'}")
    
    print(f"\nГлобальное время: {model.global_time:.2f}")


# ============================================
# 6. ТЕСТ С КВАНТОВЫМИ НЕЙРОНАМИ
# ============================================
def test_quantum():
    print("\n" + "="*50)
    print("ТЕСТ: Квантовые нейроны")
    print("="*50)
    
    from sklearn.datasets import load_digits
    from sklearn.model_selection import train_test_split
    
    digits = load_digits()
    X = digits.data / 16.0
    y = digits.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=400, random_state=42)
    
    # Скрытый слой с квантовыми нейронами
    model = TMTModel(sizes=[64, 32, 10], neuron_types=["quantum", "classic"])
    
    for epoch in range(50):
        loss = 0
        for x, y_true in zip(X_train, y_train):
            loss += model.train_step(x, y_true, lr=0.01)
        
        if epoch % 10 == 0:
            correct = sum(model.predict(x) == y for x, y in zip(X_test, y_test))
            acc = correct / len(y_test)
            print(f"Эпоха {epoch:3d} | Время: {model.global_time:8.2f} | "
                  f"Loss: {loss/len(X_train):.4f} | Acc: {acc:.2%}")
    
    correct = sum(model.predict(x) == y for x, y in zip(X_test, y_test))
    print(f"\nФинальная точность: {correct/len(y_test):.2%}")


# ============================================
# ЗАПУСК
# ============================================
if __name__ == "__main__":
    test_xor()
    test_quantum()
    print("\nГотово. t = A.")
    input("\nНажми Enter...")
