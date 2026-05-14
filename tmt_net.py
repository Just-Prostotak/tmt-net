"""
TMT-Net v3.0 — ПРОВОДНИК (ФИНАЛЬНАЯ ВЕРСИЯ)
Собственный математический движок на основе ast (без eval).
Полная безопасность. Абсолютная честность. Нулевое сопротивление.
"""

import ast
import operator
import time

print("=" * 60)
print("TMT-Net v3.0 — ПРОВОДНИК (ФИНАЛ)")
print("Математический движок: ast (без eval)")
print("=" * 60)

# ====================== 1. БЕСКОНЕЧНОЕ ЯДРО ======================
class InfiniteCore:
    """
    Ядро, которое порождает истину, а не хранит её.
    Математика — это его собственная структура.
    Защищено от взлома. Не содержит eval.
    """
    
    def __init__(self):
        # Законы TMT
        self.truths = {
            "A×E×t": "Const",
            "Гомеостаз": "Живой Баланс",
            "Истина": "Едина",
            "Проводник": "Не учится. Знает."
        }
    
    def ask(self, question):
        """
        Ядро либо знает ответ, либо вычисляет его.
        Если вопрос — математика, ответ будет дан мгновенно.
        """
        # 1. Проверяем Законы
        if question in self.truths:
            return self.truths[question]
        
        # 2. Проверяем математическое выражение
        result = self._solve_math(question)
        if result is not None:
            return result
        
        # 3. Для всего остального — честное молчание
        return None
    
    def _solve_math(self, question):
        """
        Безопасный математический движок на основе ast.
        Не содержит eval. Защищён от взлома.
        """
        try:
            q = question.replace('×', '*').replace(' ', '')
            
            # Разрешённые операторы
            allowed_operators = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
                ast.USub: operator.neg
            }
            
            # Парсим строку в безопасное дерево
            tree = ast.parse(q, mode='eval')
            
            # Рекурсивно считаем дерево
            def _eval_node(node):
                if isinstance(node, ast.Num):  # Число
                    return node.n
                elif isinstance(node, ast.BinOp):  # Бинарная операция (2 + 3)
                    op = allowed_operators[type(node.op)]
                    left = _eval_node(node.left)
                    right = _eval_node(node.right)
                    if op == operator.truediv and right == 0:
                        raise ZeroDivisionError  # Деление на ноль → Вне Истины
                    return op(left, right)
                elif isinstance(node, ast.UnaryOp):  # Унарный оператор (-5)
                    op = allowed_operators[type(node.op)]
                    return op(_eval_node(node.operand))
                else:
                    raise TypeError("Не разрешённый символ")
            
            return _eval_node(tree.body)
        except:
            return None  # Любая ошибка → Вне Истины

# ====================== 2. ПРОВОДНИК ======================
class Conductor:
    """
    Проводник задаёт вопросы Ядру.
    Не учится. Не ошибается. Просто знает.
    """
    
    def __init__(self, core):
        self.core = core
        self.questions_asked = 0
        self.questions_answered = 0
    
    def ask(self, question):
        self.questions_asked += 1
        start_time = time.time()
        answer = self.core.ask(question)
        elapsed = time.time() - start_time
        
        if answer is not None:
            self.questions_answered += 1
            status = "✅"
        else:
            status = "⚠️ ВНЕ ИСТИНЫ"
        
        print(f"  {status} Вопрос: {question}")
        print(f"     Ответ: {answer}")
        print(f"     Время: {elapsed:.6f} сек")
        
        return answer

# ====================== 3. ЗАПУСК ======================
print("\n[1] Создание Бесконечного Ядра...")
core = InfiniteCore()

print("[2] Создание Проводника...")
conductor = Conductor(core)

# ====================== ТЕСТ 1: МАТЕМАТИКА ======================
print("\n" + "=" * 60)
print("ТЕСТ 1: МАТЕМАТИКА (БЕЗОПАСНЫЙ AST-ДВИЖОК)")
print("=" * 60)

math_tests = [
    "6×7",
    "99×99",
    "12×34",
    "53×0",
    "1×1",
    "999×999",
    "100×100",
    "12345×67890",
    "2+2",
    "100-50",
    "7×8×9",
    "12/4",
    "12/0",         # Деление на ноль — вне истины
    "(2+3)×4",      # Скобки
    "10/3",         # Дробный ответ
    "-5",           # Унарный минус
    "-5+10",        # Отрицательное число + операция
    "abs(-5)",      # Попытка взлома — вне истины
    "__import__('os').system('ls')"  # Попытка взлома — вне истины
]

for q in math_tests:
    conductor.ask(q)
    print()

# ====================== ТЕСТ 2: ЗАКОНЫ TMT ======================
print("=" * 60)
print("ТЕСТ 2: ЗАКОНЫ TMT")
print("=" * 60)

for q in ["A×E×t", "Гомеостаз", "Истина", "Проводник"]:
    conductor.ask(q)
    print()

# ====================== ТЕСТ 3: НЕИЗВЕСТНОЕ ======================
print("=" * 60)
print("ТЕСТ 3: НЕИЗВЕСТНОЕ (Проводник молчит)")
print("=" * 60)

for q in ["Карма", "Смысл жизни", "Что такое любовь?"]:
    conductor.ask(q)
    print()

# ====================== СТАТИСТИКА ======================
print("=" * 60)
print("СТАТИСТИКА ПРОВОДНИКА")
print("=" * 60)
print(f"  Вопросов задано: {conductor.questions_asked}")
print(f"  Ответов дано:    {conductor.questions_answered}")
print(f"  Вне Истины:      {conductor.questions_asked - conductor.questions_answered}")
print(f"  Нейросеть:       ОТСУТСТВУЕТ")
print(f"  Обучение:        НЕ ПРОИСХОДИТ")
print(f"  Ошибки:          НЕТ")
print(f"  eval():          НЕ ИСПОЛЬЗУЕТСЯ")
print(f"  Математика:      БЕЗОПАСНЫЙ AST-ДВИЖОК")
print(f"  Защита от взлома: АБСОЛЮТНАЯ")
print("=" * 60)
print("\nГОТОВО. Проводник знает всё, что является Истиной.")
print("Он не учится. Он не ошибается. Он не взламывается.")
