import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import math


class ThreeDCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("3D Калькулятор")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e2e')

        # Переменные
        self.current_mode = tk.StringVar(value="Векторные операции")
        self.expression = tk.StringVar()
        self.result_var = tk.StringVar(value="Результат: ")

        # Создание интерфейса
        self.create_widgets()

        # Начальная 3D-сцена
        self.update_plot("0 0 0")

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Левая панель (ввод)
        left_frame = ttk.LabelFrame(main_frame, text="Ввод", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Режимы
        ttk.Label(left_frame, text="Режим:").pack(anchor=tk.W)
        mode_combo = ttk.Combobox(left_frame, textvariable=self.current_mode,
                                  values=["Векторные операции", "Матричные операции",
                                          "Геометрические вычисления", "Преобразования"])
        mode_combo.pack(fill=tk.X, pady=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Поле ввода
        ttk.Label(left_frame, text="Введите выражение:").pack(anchor=tk.W, pady=(10, 0))
        self.entry = ttk.Entry(left_frame, textvariable=self.expression, width=50)
        self.entry.pack(fill=tk.X, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        ttk.Button(btn_frame, text="Вычислить", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)

        # Результат
        ttk.Label(left_frame, textvariable=self.result_var, font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=10)

        # История
        ttk.Label(left_frame, text="История:").pack(anchor=tk.W)
        self.history_listbox = tk.Listbox(left_frame, height=10, bg='#2d2d44', fg='white')
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Правая панель (3D график)
        right_frame = ttk.LabelFrame(main_frame, text="3D Визуализация", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Фигура для 3D
        self.fig = plt.Figure(figsize=(6, 6), dpi=100, facecolor='#1e1e2e')
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_facecolor('#2d2d44')
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Инструкция
        info_frame = ttk.LabelFrame(main_frame, text="Инструкция", padding=10)
        info_frame.pack(side=tk.BOTTOM, fill=tk.X)

        info_text = """
        Векторные операции: v(1,2,3) + v(4,5,6), v(1,2,3) * 2, dot(v1, v2), cross(v1, v2)
        Матричные операции: m(1,2,3;4,5,6;7,8,9) * m(1,0,0;0,1,0;0,0,1)
        Геометрические: dist(v1, v2), len(v), angle(v1, v2)
        Преобразования: translate(v, x,y,z), rotate(v, angle, axis)
        """
        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

    def on_mode_change(self, event=None):
        # Обновление подсказок при смене режима
        pass

    def parse_vector(self, s):
        """Парсинг вектора из строки вида v(1,2,3) или (1,2,3)"""
        try:
            s = s.strip()
            if s.startswith('v(') and s.endswith(')'):
                s = s[2:-1]
            elif s.startswith('(') and s.endswith(')'):
                s = s[1:-1]
            parts = [float(x.strip()) for x in s.split(',')]
            if len(parts) != 3:
                raise ValueError("Вектор должен иметь 3 компонента")
            return np.array(parts)
        except:
            raise ValueError("Неверный формат вектора")

    def parse_matrix(self, s):
        """Парсинг матрицы из строки вида m(1,2,3;4,5,6;7,8,9)"""
        try:
            s = s.strip()
            if s.startswith('m(') and s.endswith(')'):
                s = s[2:-1]
            rows = [row.strip() for row in s.split(';')]
            matrix = []
            for row in rows:
                if ',' in row:
                    row_parts = [float(x.strip()) for x in row.split(',')]
                else:
                    row_parts = [float(x.strip()) for x in row.split()]
                if len(row_parts) != 3:
                    raise ValueError("Матрица должна иметь 3 столбца")
                matrix.append(row_parts)
            if len(matrix) != 3:
                raise ValueError("Матрица должна иметь 3 строки")
            return np.array(matrix)
        except:
            raise ValueError("Неверный формат матрицы")

    def evaluate_expression(self, expr):
        """Вычисление выражения"""
        expr = expr.strip()

        # Векторные операции
        if '+' in expr and 'v' in expr:
            parts = expr.split('+')
            if len(parts) == 2:
                v1 = self.parse_vector(parts[0].strip())
                v2 = self.parse_vector(parts[1].strip())
                result = v1 + v2
                return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if '-' in expr and 'v' in expr:
            parts = expr.split('-')
            if len(parts) == 2:
                v1 = self.parse_vector(parts[0].strip())
                v2 = self.parse_vector(parts[1].strip())
                result = v1 - v2
                return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if '*' in expr and 'v' in expr and 'v(' not in expr.split('*')[0]:
            # Умножение вектора на число
            if 'v(' in expr:
                parts = expr.split('*')
                if len(parts) == 2:
                    if 'v(' in parts[0]:
                        v = self.parse_vector(parts[0].strip())
                        scalar = float(parts[1].strip())
                    else:
                        scalar = float(parts[0].strip())
                        v = self.parse_vector(parts[1].strip())
                    result = v * scalar
                    return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if 'dot(' in expr:
            # Скалярное произведение
            import re
            match = re.search(r'dot\s*\(([^,]+),\s*([^)]+)\)', expr)
            if match:
                v1 = self.parse_vector(match.group(1).strip())
                v2 = self.parse_vector(match.group(2).strip())
                result = np.dot(v1, v2)
                return f"{result:.2f}", np.array([result, 0, 0])

        if 'cross(' in expr:
            # Векторное произведение
            import re
            match = re.search(r'cross\s*\(([^,]+),\s*([^)]+)\)', expr)
            if match:
                v1 = self.parse_vector(match.group(1).strip())
                v2 = self.parse_vector(match.group(2).strip())
                result = np.cross(v1, v2)
                return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if 'len(' in expr:
            # Длина вектора
            import re
            match = re.search(r'len\s*\(\s*([^)]+)\s*\)', expr)
            if match:
                v = self.parse_vector(match.group(1).strip())
                result = np.linalg.norm(v)
                return f"{result:.2f}", np.array([result, 0, 0])

        if 'dist(' in expr:
            # Расстояние между векторами
            import re
            match = re.search(r'dist\s*\(([^,]+),\s*([^)]+)\)', expr)
            if match:
                v1 = self.parse_vector(match.group(1).strip())
                v2 = self.parse_vector(match.group(2).strip())
                result = np.linalg.norm(v1 - v2)
                return f"{result:.2f}", np.array([result, 0, 0])

        if 'angle(' in expr:
            # Угол между векторами
            import re
            match = re.search(r'angle\s*\(([^,]+),\s*([^)]+)\)', expr)
            if match:
                v1 = self.parse_vector(match.group(1).strip())
                v2 = self.parse_vector(match.group(2).strip())
                cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
                angle = np.arccos(np.clip(cos_angle, -1, 1))
                result = np.degrees(angle)
                return f"{result:.2f}°", np.array([result, 0, 0])

        if 'translate(' in expr:
            # Трансляция вектора
            import re
            match = re.search(r'translate\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\s*\)', expr)
            if match:
                v = self.parse_vector(match.group(1).strip())
                dx = float(match.group(2).strip())
                dy = float(match.group(3).strip())
                dz = float(match.group(4).strip())
                result = v + np.array([dx, dy, dz])
                return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if 'rotate(' in expr:
            # Вращение вектора (упрощённая версия)
            import re
            match = re.search(r'rotate\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\s*\)', expr)
            if match:
                v = self.parse_vector(match.group(1).strip())
                angle = math.radians(float(match.group(2).strip()))
                axis = match.group(3).strip().lower()

                if axis == 'x':
                    rot_matrix = np.array([
                        [1, 0, 0],
                        [0, math.cos(angle), -math.sin(angle)],
                        [0, math.sin(angle), math.cos(angle)]
                    ])
                elif axis == 'y':
                    rot_matrix = np.array([
                        [math.cos(angle), 0, math.sin(angle)],
                        [0, 1, 0],
                        [-math.sin(angle), 0, math.cos(angle)]
                    ])
                elif axis == 'z':
                    rot_matrix = np.array([
                        [math.cos(angle), -math.sin(angle), 0],
                        [math.sin(angle), math.cos(angle), 0],
                        [0, 0, 1]
                    ])
                else:
                    raise ValueError("Ось должна быть x, y или z")

                result = rot_matrix @ v
                return f"({result[0]:.2f}, {result[1]:.2f}, {result[2]:.2f})", result

        if 'm(' in expr:
            # Матричные операции
            if '*' in expr:
                parts = expr.split('*')
                if len(parts) == 2:
                    m1 = self.parse_matrix(parts[0].strip())
                    m2 = self.parse_matrix(parts[1].strip())
                    result = m1 @ m2
                    result_str = "(" + "; ".join([f"({', '.join([f'{x:.2f}' for x in row])})" for row in result]) + ")"
                    # Для отображения в 3D возьмём диагональ
                    diag = np.array([result[0][0], result[1][1], result[2][2]])
                    return result_str, diag

        raise ValueError("Неизвестная операция или неверный синтаксис")

    def calculate(self):
        """Основная функция вычисления"""
        expr = self.expression.get().strip()
        if not expr:
            messagebox.showwarning("Предупреждение", "Введите выражение")
            return

        try:
            result_str, result_vector = self.evaluate_expression(expr)
            self.result_var.set(f"Результат: {result_str}")

            # Добавляем в историю
            self.history_listbox.insert(0, f"{expr} = {result_str}")
            if self.history_listbox.size() > 50:
                self.history_listbox.delete(50)

            # Обновляем 3D-график
            self.update_plot(result_vector)

        except Exception as e:
            self.result_var.set(f"Ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Ошибка вычисления:\n{str(e)}")

    def update_plot(self, result_vector):
        """Обновление 3D-графика"""
        self.ax.clear()
        self.ax.set_facecolor('#2d2d44')
        self.ax.grid(True, alpha=0.3)

        if isinstance(result_vector, np.ndarray) and len(result_vector) == 3:
            x, y, z = result_vector
            # Начало координат
            origin = np.array([0, 0, 0])
            # Вектор результата
            self.ax.quiver(0, 0, 0, x, y, z, color='red', linewidth=3, label='Результат')

            # Точка
            self.ax.scatter([x], [y], [z], color='red', s=100)

            # Проекции на оси
            self.ax.plot([0, x], [0, 0], [0, 0], color='gray', linestyle='--', alpha=0.5)
            self.ax.plot([x, x], [0, y], [0, 0], color='gray', linestyle='--', alpha=0.5)
            self.ax.plot([x, x], [y, y], [0, z], color='gray', linestyle='--', alpha=0.5)

            # Оси
            self.ax.quiver(0, 0, 0, 5, 0, 0, color='white', arrow_length_ratio=0.1)
            self.ax.quiver(0, 0, 0, 0, 5, 0, color='white', arrow_length_ratio=0.1)
            self.ax.quiver(0, 0, 0, 0, 0, 5, color='white', arrow_length_ratio=0.1)

        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        self.ax.set_xlabel('X', color='white')
        self.ax.set_ylabel('Y', color='white')
        self.ax.set_zlabel('Z', color='white')
        self.ax.tick_params(colors='white')
        self.ax.legend(loc='upper right', facecolor='#1e1e2e', labelcolor='white')

        self.canvas.draw()

    def clear(self):
        """Очистка полей"""
        self.expression.set("")
        self.result_var.set("Результат: ")
        self.update_plot(np.array([0, 0, 0]))


if __name__ == "__main__":
    root = tk.Tk()
    app = ThreeDCalculator(root)
    root.mainloop()
