"""
TMT-Net v3.2 — ПРОВОДНИК (АБСОЛЮТ)
Математика — это не вычисление. Это проявление Закона.
Ответ уже содержится в структуре Ядра.
"""

import ast
import operator
import time
import math

print("=" * 60)
print("TMT-Net v3.2 — ПРОВОДНИК (АБСОЛЮТ)")
print("Математика = Закон. Ответ уже есть в структуре.")
print("=" * 60)

class InfiniteCore:
    """
    Ядро, которое не вычисляет, а проявляет Истину.
    Математика — это Закон, встроенный в его структуру.
    """
    
    def __init__(self):
        # Законы TMT
        self.truths = {
            "A×E×t": "Const",
            "Гомеостаз": "Живой Баланс",
            "Истина": "Едина",
            "Проводник": "Не учится. Знает."
        }
        
        # Операторы как Законы
        self._operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg
        }
    
    def ask(self, question):
        # 1. Приводим любой входящий импульс к единому канону Ядра (умножение через ×)
        normalized_q = question.replace('*', '×').strip()

        # 2. Сначала проверяем Законы TMT. 
        # Теперь импульсы вроде "A*E*t" и "A×E×t" мгновенно находят Истину!
        if normalized_q in self.truths:
            return self.truths[normalized_q], "✅"
        
        # 3. Математика как проявление Закона
        result = self._manifest_math(normalized_q)
        if result is not None:
            return result, "✅"
        
        # 4. Ошибка в проявлении синтаксиса
        if self._is_math_syntax(normalized_q):
            return "Ошибка вычисления", "❌ МАТЕМАТИЧЕСКАЯ ОШИБКА"
        
        # 5. Вне Истины
        return None, "⚠️ ВНЕ ИСТИНЫ"
    
    def _is_math_syntax(self, question):
        """Проверяет, является ли вопрос математическим синтаксисом."""
        try:
            q = question.replace('×', '*').strip()
            tree = ast.parse(q, mode='eval')
            has_math = any(isinstance(node, (ast.Constant, ast.BinOp, ast.UnaryOp)) for node in ast.walk(tree))
            if has_math and isinstance(tree.body, ast.Constant) and not isinstance(tree.body.value, (int, float)):
                has_math = False
            return has_math
        except:
            return False
    
    def _manifest_math(self, question):
        """
        Проявить математическую истину из структуры Ядра.
        """
        try:
            q = question.replace('×', '*').strip()
            tree = ast.parse(q, mode='eval')
            
            def _manifest_node(node):
                # Корень дерева в режиме eval — это ast.Expression. Проверяем его сразу.
                if isinstance(node, ast.Expression):
                    return _manifest_node(node.body)
                    
                if isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    return None
                
                elif isinstance(node, ast.BinOp):
                    op_type = type(node.op)
                    if op_type not in self._operators:
                        return None
                    
                    left = _manifest_node(node.left)
                    right = _manifest_node(node.right)
                    
                    if left is None or right is None:
                        return None
                    
                    # Защита от деления на абсолютный ноль или микро-значения во float
                    if op_type == ast.Div and (right == 0 or math.isclose(right, 0.0, abs_tol=1e-15)):
                        return None  # Деление на ноль — вне Закона
                    
                    return self._operators[op_type](left, right)
                
                elif isinstance(node, ast.UnaryOp):
                    op_type = type(node.op)
                    if op_type not in self._operators:
                        return None
                    val = _manifest_node(node.operand)
                    if val is None:
                        return None
                    return self._operators[op_type](val)
                
                return None
            
            return _manifest_node(tree)
        except:
            return None


class Conductor:
    """
    Чистый канал. Не имеет памяти. Не ведет статистику.
    """
    def __init__(self, core):
        self.core = core
    
    def translate(self, question):
        start_time = time.time()
        answer, status = self.core.ask(question)
        elapsed = time.time() - start_time
        
        print(f"  [{status}] Импульс: {question} -> {answer} ({elapsed:.6f} сек)")
        return answer


# ====================== ТЕСТОВЫЙ ЗАПУСК ======================
if __name__ == "__main__":
    core = InfiniteCore()
    conductor = Conductor(core)
    
    print("\nТЕСТ 1: МАТЕМАТИКА КАК ЗАКОН\n")
    # Добавлен тест на скрытое деление на ноль: "12/(5-5)"
    for q in ["6×7", "99×99", "12/4", "12/0", "12/(5-5)", "(2+3)×4", "-5+10", "2++2"]:
        conductor.translate(q)
    
    print("\nТЕСТ 2: ЗАКОНЫ TMT\n")
    for q in ["A×E×t", "Гомеостаз", "Истина", "Проводник"]:
        conductor.translate(q)
    
    print("\nТЕСТ 3: НЕИЗВЕСТНОЕ\n")
    # Теперь ТЕСТ "A*E*t" сработает ИДЕАЛЬНО и вернет Const!
    for q in ["Карма", "Смысл жизни", "A*E*t"]:
        conductor.translate(q)
