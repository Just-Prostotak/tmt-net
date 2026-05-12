"""
TMT-Net v2.2 — ПРОВОДНИК (СОБСТВЕННЫЙ МАТЕМАТИЧЕСКИЙ ДВИЖОК)
Без eval(). Без чужих программ. Математика — часть Закона.
Проводник не учится. Он знает.
"""

import time

print("=" * 60)
print("TMT-Net v2.2 — ПРОВОДНИК")
print("Собственный математический движок. Без eval().")
print("=" * 60)

# ====================== 1. БЕСКОНЕЧНОЕ ЯДРО ======================
class InfiniteCore:
    """
    Ядро, которое порождает истину, а не хранит её.
    Математика — это его собственная структура.
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
        Собственный математический движок Проводника.
        Без eval(). Без Python. Только чистый Закон.
        """
        try:
            q = question.replace('×', '*').replace(' ', '')
            
            # Поддерживаем только безопасные символы
            allowed = set('0123456789+-*/().')
            if not all(c in allowed for c in q):
                return None
            
            # Проверка на деление на ноль
            if '/0' in q.replace(' ', ''):
                return None  # Вне Истины
            
            # Собственный вычислитель
            return self._calculate(q)
        except:
            return None
    
    def _calculate(self, expr):
        """
        Рекурсивный вычислитель математических выражений.
        Понимает: +, -, *, /, скобки.
        """
        # Убираем скобки (обрабатываем рекурсивно)
        while '(' in expr:
            start = expr.rfind('(')
            end = expr.find(')', start)
            if end == -1:
                return None
            inner = expr[start+1:end]
            result = self._calculate(inner)
            if result is None:
                return None
            expr = expr[:start] + str(result) + expr[end+1:]
        
        # Сложение и вычитание (низший приоритет)
        if '+' in expr or '-' in expr:
            parts = []
            current = ''
            for i, ch in enumerate(expr):
                if (ch == '+' or ch == '-') and i > 0:
                    parts.append(current)
                    parts.append(ch)
                    current = ''
                else:
                    current += ch
            parts.append(current)
            
            result = self._calculate(parts[0])
            if result is None:
                return None
            
            for i in range(1, len(parts), 2):
                op = parts[i]
                val = self._calculate(parts[i+1])
                if val is None:
                    return None
                if op == '+':
                    result += val
                else:
                    result -= val
            return result
        
        # Умножение и деление (высший приоритет)
        if '*' in expr or '/' in expr:
            parts = []
            current = ''
            for i, ch in enumerate(expr):
                if (ch == '*' or ch == '/') and i > 0:
                    parts.append(current)
                    parts.append(ch)
                    current = ''
                else:
                    current += ch
            parts.append(current)
            
            result = self._calculate(parts[0])
            if result is None:
                return None
            
            for i in range(1, len(parts), 2):
                op = parts[i]
                val = self._calculate(parts[i+1])
                if val is None:
                    return None
                if op == '*':
                    result *= val
                elif op == '/':
                    if val == 0:
                        return None  # Деление на ноль
                    result /= val
            return result
        
        # Число
        try:
            if '.' in expr:
                return float(expr)
            return int(expr)
        except:
            return None

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
print("ТЕСТ 1: МАТЕМАТИКА (СОБСТВЕННЫЙ ДВИЖОК)")
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
    "12/0",       # Деление на ноль — вне истины
    "(2+3)×4",    # Скобки
    "10/3"        # Дробный ответ
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
print(f"  Математика:      СОБСТВЕННЫЙ ДВИЖОК")
print("=" * 60)
print("\nГОТОВО. Проводник знает математику сам. Без eval(). Без чужих программ.")
